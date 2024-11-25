import asyncio
import os
import random
import re
import sys
import time
import aiohttp
from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from config import Config, temp
from queue import Queue
from yt_dlp import YoutubeDL, DownloadError
from utility.database import db
from utility import *
from utility.helper import fix_thumb



# Upload Video 🍃
async def uploadVideo(bot:Client, query: CallbackQuery, message, path: str, quality:str, item: object = None):
    userId = query.from_user.id
    ms = await message.edit("⚠️ ** ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ... **\n** ᴛʀʏɪɴɢ ᴛᴏ ᴜᴘʟᴏᴀᴅ... **")

    # uuid = f"{Config.BOT_USERNAME}_{str_to_b64(str(fileInfo['msg_id']))}"
    if item:
        videoInfo = item
    else:
        videoInfo = temp.VIDEOINFO[userId]

    thumbnail_filename = f"thumbnail_{random.randint(1000, 9999)}.jpg"
    await download_thumbnail(videoInfo["thumbnail"], thumbnail_filename)
    width, height, thumb = await fix_thumb(thumbnail_filename)
    file_size = humanbytes(os.path.getsize(path))
    caption = f"> **File Name:** `{videoInfo['title']}`\n\n> **File Size:** `{file_size}`\n> **Quality:** `{quality}`\n> **Duration:** `{videoInfo['duration']}`\n> **Powered By - **[{Config.BOT_USERNAME}](https://t.me/{Config.BOT_USERNAME})** 🔞**"


    try:
        filz = await bot.send_video(chat_id=Config.DUMP_VIDEOS, video=path, progress=progress_for_pyrogram, thumb=thumb, caption=caption, progress_args=("🌨️ ** ᴜᴘʟᴏᴀᴅɪɴɢ sᴛᴀʀᴛᴇᴅ.... **", ms, time.time()))
        await db.add_files(userId, filz.video.file_id, videoInfo["title"], file_size, quality, videoInfo["duration"])
        uuid = f"{Config.BOT_USERNAME}_{str_to_b64(str(filz.id))}"
        await bot.copy_message(query.from_user.id, filz.chat.id, filz.id,  reply_markup=InlineKeyboardMarkup([[
                            InlineKeyboardButton(
                                "💫 sʜᴀʀᴇ ɴᴏᴡ 💫",
                                url=f"https://t.me/share/url?url=https://t.me/{Config.BOT_USERNAME}?start={uuid}",
                            )
                        ]]))
        os.remove(path)
        os.remove(thumb)
        try:
            if item:
                temp.QUEUE.pop(userId)
            else:
                temp.VIDEOINFO.pop(userId)
        except:
            pass
        return await ms.delete()
    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        return await ms.edit('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

# Single Download 🍃
async def singleDownload(bot:Client, query: CallbackQuery, link: str):
    userId = query.from_user.id
    await animated_loading(query, "**Please Wait Loading...**")

    if userId not in temp.VIDEOINFO:
        videoInfo = await getVideoInfo(link)
        temp.VIDEOINFO.update({userId: {"link": link, **videoInfo}})

    else:
        videoInfo = temp.VIDEOINFO[userId]

    if not videoInfo:
        return await query.message.edit("Something went wrong check your link !")
    
    qualityBtn = [[InlineKeyboardButton(f"{key} {'[sᴅ]' if int(key.replace('p', '').strip()) <= 480 else '[ʜᴅ]'}", f'quality_{key}') ]for key in videoInfo["videos"].keys()]
    
    await query.message.edit(text="**Chose your desire quality**", reply_markup=InlineKeyboardMarkup(qualityBtn))

# Queue Download
async def queueDownload(bot: Client, query: CallbackQuery):

    userId = query.from_user.id
    arrayVideoInfo = temp.QUEUE[userId]

    for idx, item in enumerate(arrayVideoInfo):
        ms = await query.message.reply_text(f"** 📦 Downloading Video From Queue {idx+1} **")
        userId = query.from_user.id
        queue = Queue()

        sanitized_title = re.sub(r'[<>:"/\\|?*]', '', item.get('title'))
        download_path = os.path.join(f"downloads/{userId}", f"{sanitized_title}.mkv")

        ydl_opts = {
        "outtmpl": download_path,
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "progress_hooks": [lambda d: progress_hook(d, queue)],
        }

        # Define the blocking function for yt-dlp
        def download_video():
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([item["videos"].get(item["quality"])])

        # Run the blocking download function in a thread
        loop = asyncio.get_event_loop()
        progress_task = asyncio.create_task(handle_progress(queue, ms))

        try:
            # Run yt-dlp in a separate thread
            await loop.run_in_executor(None, download_video)
        except DownloadError:
            await ms.edit("**Sorry, an error occurred during the download. ❌**")
            queue.put(None)
            await progress_task
            return
        finally:
            queue.put(None)
            await progress_task
            await ms.edit("**Download completed successfully! ✅**")
        
        await uploadVideo(bot, query, ms, download_path, item["quality"], item)
    
    await query.message.reply_text("<b>ᴀʟʟ ᴠɪᴅᴇᴏs ᴏғ ᴛʜɪs ᴘʟᴀʏʟɪsᴛ ɪs ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ✅</b>\n\n<b> 🍀 Developer </b> <a href=https://t.me/Snowball_official>ѕησωвαℓℓ ❄️</a>", disable_web_page_preview=True,)

# SpankbangPlaylistDownload
async def spankbangPlaylistDownload(bot: Client, query: CallbackQuery):
    userId = query.from_user.id

    spankbangPlaylistArray = temp.PLAYLIST_DOWNLOAD[userId]

    for link in spankbangPlaylistArray:
        try:
            ms = await query.message.reply_text(f"** 📦 Downloading Video From Playlist **")
            queue = Queue()
            videoInfo = await getVideoInfo(link)
            quality = next(reversed(videoInfo.get("videos")))
            sanitized_title = re.sub(r'[<>:"/\\|?*]', '', videoInfo.get('title'))
            filePreFound = await db.get_file(sanitized_title, quality)
            if filePreFound:
                for file in filePreFound:
                    caption = f'> **File Name:** `{file["file_name"]}`\n\n> **File Size:** `{file["file_size"]}`\n> **Quality:** `{file["file_quality"]}`\n> **Duration:** `{file["file_duration"]}`\n> **Powered By - **[{Config.BOT_USERNAME}](https://t.me/{Config.BOT_USERNAME})** 🔞**'
                    await bot.send_cached_media(chat_id=userId, file_id=file["file_id"], caption=caption)
                    return
                
            download_path = os.path.join(f"downloads/{userId}", f"{sanitized_title}.mkv")

            ydl_opts = {
                "outtmpl": download_path,
                "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                "progress_hooks": [lambda d: progress_hook(d, queue)],
            }

            # Define the blocking function for yt-dlp
            def download_video():
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([videoInfo["videos"].get(quality)])

            # Run the blocking download function in a thread
            loop = asyncio.get_event_loop()
            progress_task = asyncio.create_task(handle_progress(queue, ms))

            try:
                # Run yt-dlp in a separate thread
                await loop.run_in_executor(None, download_video)
            except DownloadError:
                await ms.edit("**Sorry, an error occurred during the download. ❌**")
                queue.put(None)
                await progress_task
                return
            finally:
                queue.put(None)
                await progress_task

            await uploadVideo(bot, query, ms, download_path, quality, videoInfo)
        except Exception as e:
            print(
            "Error on line {}".format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
        )