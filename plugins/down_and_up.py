import sys
import aiohttp
import requests
import asyncio
import os
import random
import time
from bs4 import BeautifulSoup
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from youtube_dl import YoutubeDL, DownloadError
from config import Config, temp
from helper.utils import (
    client,
    fix_thumb,
    progress_for_pyrogram,
    format_duration,
    get_video_durations,
    get_thumbnail,
    humanbytes,
    download_thumbnail,
    extract_m3u8_url,
    download_m3u8_with_ffmpeg,
    start_clone_bot,
    split_file_by_size,
)
from helper.database import db
from helper.utils import str_to_b64


async def cache_file(fileInfo, url, bot, query, user_id, user_status):
    if fileInfo:
        for fileInfo in fileInfo:
            if str(fileInfo["link"]).endswith(url):
                try:
                    if (
                        user_status["plan"] == "free"
                        and user_id not in Config.ADMIN
                        and Config.SHORTENER_API
                        and user_id not in temp.TOKEN
                    ):

                        uuid = f"{Config.BOT_USERNAME}_{str_to_b64(str(fileInfo['msg_id']))}"
                        shorturl = f"{Config.SHORTENER_API}https://t.me/{Config.BOT_USERNAME}?start={uuid}&format=text"
                        url = await fetch_shorturl(shorturl=shorturl)
                        file = await bot.get_messages(
                            Config.DUMP_VIDEOS, int(fileInfo["msg_id"])
                        )
                        btn = [[InlineKeyboardButton("📥 Download 📥", url=f"{url}")]]
                        await bot.send_message(
                            chat_id=user_id,
                            text=f"{file.caption}\n\n👑 Upgrade to get direct files /upgrade",
                            entities=file.caption_entities,
                            reply_markup=InlineKeyboardMarkup(btn),
                        )

                    else:
                        uuid = f"{Config.BOT_USERNAME}_{str_to_b64(str(fileInfo['msg_id']))}"
                        await bot.copy_message(
                            query.from_user.id,
                            Config.DUMP_VIDEOS,
                            int(fileInfo["msg_id"]),
                            reply_markup=InlineKeyboardMarkup(
                                [
                                    [
                                        InlineKeyboardButton(
                                            "🌟 sʜᴀʀᴇ ɴᴏᴡ 🌟",
                                            url=f"https://t.me/share/url?url=https://t.me/{Config.BOT_USERNAME}?start={uuid}",
                                        )
                                    ]
                                ]
                            ),
                        )
                except:
                    await bot.send_video(
                        chat_id=query.message.chat.id,
                        video=fileInfo["file_id"],
                        caption=fileInfo["caption"],
                    )

        await query.message.delete()
        return True
    else:
        return False


# Function to print the download progress
def print_progress(d, ms):

    if d["status"] == "downloading":
        message = f"ㅤ\n**Downloading:** `{d['_percent_str']}` ** of ** `{d['_total_bytes_str']}` ** at ** `{d['_speed_str']}`\n\n** ETA: ** `{d['_eta_str']}`"
        try:
            ms.edit(message, disable_web_page_preview=True)
        except:
            pass
    elif d["status"] == "finished":
        try:
            ms.edit(f"** Download finished, now converting... ✅**")
        except:
            pass


async def download(url, query, ms):

    file_name = "%(title)s-%(id)s.%(ext)s"

    if "xhamster" in url:
        html_parser = requests.get(url)
        soup = BeautifulSoup(html_parser.text, "html5lib")
        url = soup.find(
            "a",
            attrs={
                "class": "player-container__no-player xplayer xplayer-fallback-image xh-helper-hidden"
            },
        )["href"]
        file_name = (
            f"{soup.find('h1', attrs={'data-testid': 'font-container'}).text}.mp4"
        )

    ydl_opts = {
        "outtmpl": os.path.join(f"downloads/{query.from_user.id}", file_name),
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        # "progress_hooks": [lambda d: print_progress(d, ms)],
    }
    loop = asyncio.get_event_loop()
    with YoutubeDL(ydl_opts) as ydl:
        try:
            await loop.run_in_executor(None, lambda: ydl.download([url]))
        except DownloadError:
            await ms.edit("Sorry, an error")
            return 0


async def download_javhd(message, url, userid):
    await message.edit(
        f"🔗 Lɪɴᴋ :- `{url}`\n\n **Fetching Downloadable Link ♻️**\n\n**⚠️ It might take few seconds as it's using some algorithm to fetch downloadable link **\n> Have Patiences Don't Be Too Horny"
    )
    download_link = await extract_m3u8_url(url)
    fileName = url.split("/")[-2].capitalize()
    short_name = fileName[:215] + "..." if len(fileName) > 218 else fileName
    download_filename = f"{short_name}.mp4"
    output_file = f"downloads/{userid}/{download_filename}"
    if download_link:
        await download_m3u8_with_ffmpeg(
            message=message, url=download_link, output_file=output_file
        )
    else:
        await message.edit("**Unable to fetch the downloadable link.**")
        return 0


async def fetch_shorturl(shorturl):
    async with aiohttp.ClientSession() as session:
        async with session.get(shorturl) as response:
            return await response.text()


async def OnlyUpload(
    bot,
    query,
    download_dir,
    file_path,
    thumbnail_filename,
    file_size,
    ms,
    app,
    user_id,
    user_status,
    downloadurl,
):
    try:
        await ms.delete()
        for file in os.listdir(download_dir):

            if not file.endswith((".mp4", ".mkv")):
                continue

            ms = await query.message.reply_text(
                "**⚠️ Please Wait....**\n\n**Trying to Upload ☁️**"
            )
            file_path = os.path.join(download_dir, file)
            file_size = os.path.getsize(file_path)

            duration = await format_duration(await get_video_durations(file_path))
            size = humanbytes(file_size)
            caption = f"> **📁 File Name:** `{file}`\n\n> **💾 File Size:** `{size}`\n\n> **⏰ Duration:** `{duration}`\n\n> **Powered By - **[{Config.BOT_USERNAME}](https://t.me/{Config.BOT_USERNAME})** 🔞"
            width, height, thumb = await fix_thumb(thumbnail_filename)

            if app:
                filz = await app.send_video(
                    Config.DUMP_VIDEOS,
                    video=file_path,
                    thumb=thumb,
                    width=width,
                    height=height,
                    caption=caption,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        "⚠️ Please wait...\n\n**Uploading started... ❄️**",
                        ms,
                        time.time(),
                    ),
                )
            else:
                filz = await bot.send_video(
                    Config.DUMP_VIDEOS,
                    video=file_path,
                    thumb=thumb,
                    width=width,
                    height=height,
                    caption=caption,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        "⚠️ Please wait...\n\n**Uploading started... ❄️**",
                        ms,
                        time.time(),
                    ),
                )

            fileInfo = await bot.get_messages(Config.DUMP_VIDEOS, filz.id)
            await db.add_files(
                downloadurl,
                filz.id,
                (
                    fileInfo.animation.file_id
                    if fileInfo.animation
                    else fileInfo.video.file_id
                ),
                (
                    fileInfo.video.file_name
                    if fileInfo.video
                    else fileInfo.animation.file_name
                ),
                (
                    fileInfo.video.file_size
                    if fileInfo.video
                    else fileInfo.animation.file_size
                ),
                (
                    fileInfo.video.mime_type.split("/")[0]
                    if fileInfo.video
                    else fileInfo.animation.mime_type.split("/")[0]
                ),
                (
                    fileInfo.video.mime_type
                    if fileInfo.video
                    else fileInfo.animation.mime_type
                ),
                fileInfo.caption,
            )

            if (
                user_status["plan"] == "free"
                and user_id not in Config.ADMIN
                and Config.SHORTENER_API
                and user_id not in temp.TOKEN
            ):
                uuid = f"{Config.BOT_USERNAME}_{str_to_b64(str(filz.id))}"
                shorturl = f"{Config.SHORTENER_API}https://t.me/{Config.BOT_USERNAME}?start={uuid}&format=text"
                url = await fetch_shorturl(shorturl=shorturl)
                btn = [[InlineKeyboardButton("📥 Download 📥", url=f"{url}")]]
                await bot.send_message(
                    chat_id=user_id,
                    text=f"{caption}\n\n**[📥 Click Here To Download Now 📥]({url})**\n\n**👑 Upgrade to get direct files /upgrade **",
                    reply_markup=InlineKeyboardMarkup(btn),
                )
            else:
                uuid = f"{Config.BOT_USERNAME}_{str_to_b64(str(filz.id))}"
                await bot.copy_message(
                    user_id,
                    filz.chat.id,
                    filz.id,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "💫 sʜᴀʀᴇ ɴᴏᴡ 💫",
                                    url=f"https://t.me/share/url?url=https://t.me/{Config.BOT_USERNAME}?start={uuid}",
                                )
                            ]
                        ]
                    ),
                )

            os.remove(file_path)
            await ms.delete()

    except Exception as e:
        print(
            "Error on line {}".format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
        )


async def upload(bot, query, thumbnail_filename, ms, downloadurl, user_bot=None):
    try:
        download_dir = f"downloads/{query.from_user.id}"
        user_id = query.from_user.id
        user_status = await db.get_user_status(user_id)

        for file in os.listdir(download_dir):
            if not file.endswith((".mp4", ".mkv")):
                continue

            file_path = os.path.join(download_dir, file)
            file_size = os.path.getsize(file_path)

            if file_size > 4000 * 1024 * 1024:
                if user_bot:
                    app = await start_clone_bot(client(user_bot["session"]))
                else:
                    app = None

                await ms.edit(
                    "** Tʜᴇ ᴠɪᴅᴇᴏ ғɪʟᴇ ɪs ʟᴀʀɢᴇʀ ᴛʜᴀɴ 4GB, sᴏ I ɴᴇᴇᴅ ᴛᴏ sᴘʟɪᴛ ɪᴛ ɪɴᴛᴏ sᴍᴀʟʟᴇʀ ᴘᴀʀᴛs ᴛᴏ ᴜᴘʟᴏᴀᴅ ɪᴛ. **\n\nᴘʀᴏᴄᴇssɪɴɢ ♻️"
                )
                await split_file_by_size(
                    input_file=file_path,
                    max_part_size_mb=4000 if app else 2000,
                    file_name=file,
                    user_id=user_id,
                )
                os.remove(file_path)
                await OnlyUpload(
                    bot=bot,
                    query=query,
                    download_dir=download_dir,
                    file_path=file_path,
                    thumbnail_filename=thumbnail_filename,
                    file_size=file_size,
                    ms=ms,
                    app=app if app else None,
                    user_id=user_id,
                    user_status=user_status,
                    downloadurl=downloadurl,
                )

                if user_bot:
                    await app.stop()

            elif file_size > 2000 * 1024 * 1024 and not user_bot:

                await ms.edit(
                    "** Tʜᴇ ᴠɪᴅᴇᴏ ғɪʟᴇ ɪs ʟᴀʀɢᴇʀ ᴛʜᴀɴ 2GB, sᴏ I ɴᴇᴇᴅ ᴛᴏ sᴘʟɪᴛ ɪᴛ ɪɴᴛᴏ sᴍᴀʟʟᴇʀ ᴘᴀʀᴛs ᴛᴏ ᴜᴘʟᴏᴀᴅ ɪᴛ. **\n\nᴘʀᴏᴄᴇssɪɴɢ ♻️"
                )
                await split_file_by_size(
                    input_file=file_path,
                    max_part_size_mb=2000,
                    file_name=file,
                    user_id=user_id,
                )
                os.remove(file_path)
                await OnlyUpload(
                    bot=bot,
                    query=query,
                    download_dir=download_dir,
                    file_path=file_path,
                    thumbnail_filename=thumbnail_filename,
                    file_size=file_size,
                    ms=ms,
                    app=None,
                    user_id=user_id,
                    user_status=user_status,
                    downloadurl=downloadurl,
                )

            elif (
                file_size > 2000 * 1024 * 1024
                and file_size <= 4000 * 1024 * 1024
                and user_bot
            ):

                app = await start_clone_bot(client(user_bot["session"]))

                await OnlyUpload(
                    bot=bot,
                    query=query,
                    download_dir=download_dir,
                    file_path=file_path,
                    thumbnail_filename=thumbnail_filename,
                    file_size=file_size,
                    ms=ms,
                    app=app,
                    user_id=user_id,
                    user_status=user_status,
                    downloadurl=downloadurl,
                )

                await app.stop()

            else:
                await OnlyUpload(
                    bot=bot,
                    query=query,
                    download_dir=download_dir,
                    file_path=file_path,
                    thumbnail_filename=thumbnail_filename,
                    file_size=file_size,
                    ms=ms,
                    app=None,
                    user_id=user_id,
                    user_status=user_status,
                    downloadurl=downloadurl,
                )

            os.remove(thumbnail_filename)

            break

    except Exception as e:
        print(
            "Error on line {}".format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e
        )


async def queue_download(bot, query, url):

    fileInfo = await db.get_files(
        "https://www.eporner.com" + url if url.startswith("/dload") else url
    )
    user_id = query.from_user.id
    user_status = await db.get_user_status(user_id)

    cache = await cache_file(fileInfo, url, bot, query, user_id, user_status)
    if cache:
        return

    user_id = query.from_user.id
    download_dir = f"downloads/{user_id}"
    os.makedirs(download_dir, exist_ok=True)
    ms = await query.message.reply_text(
        f"🔗 Link :- `{url}`\n\n**Downloading...**\n\n__**⚠️ File is downloading in the background to avoid being stuck.**__"
    )

    download_success = False

    if "javhd.today" in url or "javhd.icu" in url or "javtsunami.com" in url or "javgiga.com" in url:
        download_success = await download_javhd(ms, url, user_id)
    elif "eporner.com" in url:
        rs = requests.get(url)
        soup = BeautifulSoup(rs.text, "html5lib")
        download_links = soup.find("div", attrs={"class": "dloaddivcol"}).find_all("a")
        new_url = "https://www.eporner.com" + download_links[-1]["href"]
        download_success = await download(new_url, query, ms)

    else:
        download_success = await download(url, query, ms)

    if download_success == 0:
        await ms.edit("** Download Failed ❌ **")
        return

    print("Download Done ✅")
    await ms.edit("**Fetching Thumbnail.... 🔃**")
    thumb_url = await get_thumbnail(video_url=url)
    thumbnail_filename = f"thumbnail_{random.randint(1000, 9999)}.jpg"
    await download_thumbnail(thumb_url, thumbnail_filename)

    user_bot = None
    for admin_id in Config.ADMIN:
        try:
            user_bot = await db.get_user_bot(admin_id)
            if user_bot:
                break
        except Exception as e:
            print(f"Failed to get user bot for admin {admin_id}: {e}")

    await upload(
        bot=bot,
        query=query,
        thumbnail_filename=thumbnail_filename,
        ms=ms,
        user_bot=user_bot,
        downloadurl=url,
    )


async def single_download(bot, query, url, default_url=None):
    fileInfo = await db.get_files(
        "https://www.eporner.com" + url if url.startswith("/dload") else url
    )
    user_id = query.from_user.id
    user_status = await db.get_user_status(user_id)

    cache = await cache_file(fileInfo, url, bot, query, user_id, user_status)
    if cache:
        return

    user_id = query.from_user.id
    download_dir = f"downloads/{user_id}"
    os.makedirs(download_dir, exist_ok=True)
    ms = await query.message.edit(
        "**Downloading...**\n\n__**⚠️ File is downloading in the background to avoid being stuck.**__"
    )

    download_success = False

    if "javhd.today" in url or "javhd.icu" in url or "javtsunami.com" in url or "javgiga.com" in url:
        download_success = await download_javhd(ms, url, user_id)
        if download_success == 0:
            await ms.edit("** Download Failed ❌ **")
            return
    else:
        if url.startswith("/dload"):
            url = "https://www.eporner.com" + url
        download_success = await download(url, query, ms)
        if download_success == 0:
            await ms.edit("** Download Failed ❌ **")
            return

    print("Download Done ✅")
    await ms.edit("**Fetching Thumbnail.... 🔃**")

    thumbnail_url = await get_thumbnail(default_url if default_url else url)
    thumbnail_filename = f"thumbnail_{random.randint(1000, 9999)}.jpg"
    await download_thumbnail(thumbnail_url, thumbnail_filename)

    user_bot = None
    for admin_id in Config.ADMIN:
        try:
            user_bot = await db.get_user_bot(admin_id)
            if user_bot:
                break
        except Exception as e:
            print(f"Failed to get user bot for admin {admin_id}: {e}")

    await upload(
        bot=bot,
        query=query,
        thumbnail_filename=thumbnail_filename,
        ms=ms,
        user_bot=user_bot,
        downloadurl=url,
    )
