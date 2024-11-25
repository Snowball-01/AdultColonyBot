import asyncio
import os
import re
import shutil
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    CallbackQuery,
    MessageEntity
)
import requests
from utility.database import db
from plugins.down_and_up import queueDownload, singleDownload, uploadVideo, spankbangPlaylistDownload
from config import Config, temp, Txt
from queue import Queue
from yt_dlp import YoutubeDL, DownloadError
from utility import *


@Client.on_callback_query(filters.regex(r"^add_queue"))
async def handle_queue(bot: Client, query: CallbackQuery):
    user = query.from_user.id
    await animated_loading(query, "**📂 Adding to queue**")
    videoInfo = await getVideoInfo(query.message.reply_to_message.text)
    qualityBtn = [[InlineKeyboardButton(f"{key} {'[sᴅ]' if int(key.replace('p', '').strip()) <= 480 else '[ʜᴅ]'}", f'queuequality_{key}') ]for key in videoInfo["videos"].keys()]
    if is_video_in_queue(temp.QUEUE, user, videoInfo):
        return await query.message.edit(text="** Video is already in queue 🍃 **")
    temp.QUEUE.setdefault(user, []).append(videoInfo)
    await query.message.edit(text="**Chose your desire quality**", reply_markup=InlineKeyboardMarkup(qualityBtn))
    


@Client.on_callback_query(filters.regex(r"^queuequality_"))
async def handle_queue_quality(bot: Client, query: CallbackQuery):
    userId = query.from_user.id
    quality = query.data.split('_')[1]
    arrayVideoInfo = temp.QUEUE[userId]
    arrayVideoInfo[-1]["quality"] = quality
    await query.message.edit(
        "**ᴛʜɪs ʟɪɴᴋ ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ sᴜᴄᴄᴇssғᴜʟʟʏ ✅**",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("✔ Done ✔", callback_data="done_queue")]]
        ),
    )

@Client.on_callback_query(filters.regex(r"^done_queue"))
async def handle_done_queue(bot: Client, query: CallbackQuery):
    userId = query.from_user.id


    if userId not in temp.QUEUE:
        return await query.answer(
            f"Hey {query.from_user.first_name}\n\nYᴏᴜʀ ǫᴜᴇᴜᴇ ɪs ᴇᴍᴘᴛʏ. Fɪʀsᴛ ᴀᴅᴅ ʟɪɴᴋs ᴛᴏ ǫᴜᴇᴜᴇ ᴛʜᴇɴ ᴜsᴇ ᴛʜɪs ʙᴜᴛᴛᴏɴ",
            show_alert=True,
        )

    if userId in temp.IN_QUEUE_DOWNLOADS:
        return await query.answer(
            f"Hey {query.from_user.first_name}\n\n📩 Dᴏᴡɴʟᴏᴀᴅɪɴɢ ɪs ᴀʟʀᴇᴀᴅʏ sᴛᴀʀᴛᴇᴅ ɪɴ ǫᴜᴇᴜᴇ. Hᴀᴠᴇ ᴘᴀᴛɪᴇɴᴄᴇ ᴡʜɪʟᴇ ɪᴛ's ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ",
            show_alert=True,
        )

    temp.IN_QUEUE_DOWNLOADS.append(userId)
    
    await queueDownload(bot, query)

    temp.QUEUE.pop(userId, None)
    temp.IN_QUEUE_DOWNLOADS.remove(userId)


@Client.on_callback_query(filters.regex(r"^spankbang_playlist"))
async def handle_spankbang_playlist(bot: Client, query: CallbackQuery):
    user = query.from_user.id

    if user in temp.IN_QUEUE_DOWNLOADS:
        return await query.answer(
            f"Hᴇʏ {query.from_user.first_name},\nᴘʟᴀʏʟɪsᴛ ɪs ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ. Hᴀᴠᴇ ᴘᴀᴛɪᴇɴᴄᴇ ᴡʜɪʟᴇ ɪᴛ's ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ. 📥",
            show_alert=True,
        )

    temp.IN_QUEUE_DOWNLOADS.append(user)
    await query.message.delete()
    ms = await query.message.reply_text("**ᴘʟᴀʏʟɪsᴛ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ɪs sᴛᴀʀᴛᴇᴅ ✔**")

    # handle spankbang playlist issue
    await spankbangPlaylistDownload(bot, query)

    temp.PLAYLIST_DOWNLOAD.pop(user, None)
    await query.message.reply_text(
        "<b>ᴀʟʟ ᴠɪᴅᴇᴏs ᴏғ ᴛʜɪs ᴘʟᴀʏʟɪsᴛ ɪs ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ✅</b>\n\n<b> 🍀 Developer </b> <a href=https://t.me/Snowball_official>ѕησωвαℓℓ ❄️</a>",
        reply_to_message_id=ms.id,
        disable_web_page_preview=True,
    )

@Client.on_callback_query(filters.regex(r"^download_file"))
async def handle_file(bot: Client, query: CallbackQuery):
    link = query.message.reply_to_message.text
    user = query.from_user.id

    if user in temp.IN_QUEUE_DOWNLOADS:
        return await query.answer(
            f"Hᴇʏ {query.from_user.first_name},\nDᴏᴡɴʟᴏᴀᴅ ɪs ᴀʟʀᴇᴀᴅʏ sᴛᴀʀᴛᴇᴅ ʜᴀᴠᴇ ᴘᴀᴛɪᴇɴᴄᴇ ᴡʜɪʟᴇ ɪᴛ's ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ. 📥",
            show_alert=True,
        )
    else:
        temp.IN_QUEUE_DOWNLOADS.append(user)
    
    await singleDownload(bot, query, link)


@Client.on_callback_query(filters.regex("^upgrade"))
async def handle_upgrade_callback(bot: Client, query: CallbackQuery):

    btn = [
        [InlineKeyboardButton("ᴘᴀʏ ᴛᴏ ᴀᴅᴍɪɴ", url="https://t.me/Snowball_Official")],
        [InlineKeyboardButton("ᴄʟᴏsᴇ ✘", callback_data="close")],
    ]
    markup = InlineKeyboardMarkup(btn)
    await query.message.edit(Txt.UPGRADE_MSG, reply_markup=markup)


@Client.on_callback_query(filters.regex(r'^quality_'))
async def qualityDownload(bot: Client, query: CallbackQuery):
    userId = query.from_user.id

    # Check if user has a valid video info in the temporary queue
    if userId not in temp.VIDEOINFO:
        return await query.answer(
            text=(
                f"Hey {query.from_user.first_name},\n"
                "Your queue has been cleared. If you want to download this video, please send it again."
            ),
            show_alert=True,
        )

    # Notify user of the download process
    ms = await query.message.edit("**Downloading 📦**")
    quality = query.data.split('_')[1]
    videoInfo = temp.VIDEOINFO[userId]
    queue = Queue()

    # Sanitize file name
    sanitized_title = re.sub(r'[<>:"/\\|?*]', '', videoInfo.get('title'))

    # Check for pre-cached file
    filePreFound = await db.get_file(sanitized_title, quality)
    if filePreFound:
        for file in filePreFound:
            caption = (
                f'> **File Name:** `{file["file_name"]}`\n\n'
                f'> **File Size:** `{file["file_size"]}`\n'
                f'> **Quality:** `{file["file_quality"]}`\n'
                f'> **Duration:** `{file["file_duration"]}`\n'
                f'> **Powered By - **[{Config.BOT_USERNAME}](https://t.me/{Config.BOT_USERNAME})** 🔞**'
            )
            await bot.send_cached_media(
                chat_id=userId, file_id=file["file_id"], caption=caption
            )
            return

    # Define download path
    download_path = os.path.join(f"downloads/{userId}", f"{sanitized_title}.mkv")

    # yt-dlp options
    ydl_opts = {
        "outtmpl": download_path,
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "progress_hooks": [lambda d: progress_hook(d, queue)],
    }

    # Define the blocking download function
    def download_video():
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([videoInfo["videos"].get(quality)])

    # Use asyncio.run_in_executor to run blocking downloads
    loop = asyncio.get_running_loop()  # Use the running event loop
    progress_task = asyncio.create_task(handle_progress(queue, ms))

    try:
        # Execute download in a thread pool
        await loop.run_in_executor(None, download_video)
    except DownloadError:
        await ms.edit("**Sorry, an error occurred during the download. ❌**")
    finally:
        queue.put(None)  # Signal progress task to exit
        await progress_task  # Ensure progress task completes

    # Finalize and upload the video
    if os.path.exists(download_path):
        await ms.edit("**Download completed successfully! ✅**")
        await uploadVideo(bot, query, ms, download_path, quality)
    else:
        await ms.edit("**Download failed. ❌**")

    # Clean up user from IN_QUEUE_DOWNLOADS
    if userId in temp.IN_QUEUE_DOWNLOADS:
        temp.IN_QUEUE_DOWNLOADS.remove(userId)



@Client.on_message(filters.private & filters.command("cc"))
async def handle_clear_queue(bot: Client, message: Message):

    user = message.from_user.id

    if user in temp.QUEUE:
        temp.QUEUE.pop(user)
        if os.path.exists(f"downloads/{user}"):
            shutil.rmtree(f"downloads/{user}")

    if user in temp.VIDEOINFO:
        temp.VIDEOINFO.pop(user)
        if os.path.exists(f"downloads/{user}"):
            shutil.rmtree(f"downloads/{user}")

    if user in temp.PLAYLIST_DOWNLOAD:
        temp.PLAYLIST_DOWNLOAD.pop(user)
        if os.path.exists(f"downloads/{user}"):
            shutil.rmtree(f"downloads/{user}")

    if user in temp.IN_QUEUE_DOWNLOADS:
        temp.IN_QUEUE_DOWNLOADS.remove(user)
        if os.path.exists(f"downloads/{user}"):
            shutil.rmtree(f"downloads/{user}")

    await message.reply_text(
        "**ǫᴜᴇᴜᴇ ᴄʟᴇᴀʀᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ✅**", reply_to_message_id=message.id
    )
