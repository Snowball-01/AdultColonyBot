import asyncio
import os
import shutil
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    CallbackQuery,
)
import requests
from helper.database import db
from plugins.down_and_up import single_download, queue_download
from config import Config, temp, Txt


@Client.on_callback_query(filters.regex(r"^add_queue"))
async def handle_queue(bot: Client, query: CallbackQuery):
    await query.message.edit("**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...**")
    user = query.from_user.id
    url = query.message.reply_to_message.text

    temp.QUEUE.setdefault(user, []).append(url)
    await query.message.edit(
        "**ᴛʜɪs ʟɪɴᴋ ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ sᴜᴄᴄᴇssғᴜʟʟʏ ✅**",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("✔ Done ✔", callback_data="done_queue")]]
        ),
    )


@Client.on_callback_query(filters.regex(r"^done_queue"))
async def handle_done_queue(bot: Client, query: CallbackQuery):
    user = query.from_user.id

    if user not in temp.QUEUE:
        return await query.answer(
            f"Hey {query.from_user.first_name}\n\nYᴏᴜʀ ǫᴜᴇᴜᴇ ɪs ᴇᴍᴘᴛʏ. Fɪʀsᴛ ᴀᴅᴅ ʟɪɴᴋs ᴛᴏ ǫᴜᴇᴜᴇ ᴛʜᴇɴ ᴜsᴇ ᴛʜɪs ʙᴜᴛᴛᴏɴ",
            show_alert=True,
        )

    if user in temp.PENDING_DOWNLOADS:
        return await query.answer(
            f"Hey {query.from_user.first_name}\n\n📩 Dᴏᴡɴʟᴏᴀᴅɪɴɢ ɪs ᴀʟʀᴇᴀᴅʏ sᴛᴀʀᴛᴇᴅ ɪɴ ǫᴜᴇᴜᴇ. Hᴀᴠᴇ ᴘᴀᴛɪᴇɴᴄᴇ ᴡʜɪʟᴇ ɪᴛ's ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ",
            show_alert=True,
        )

    temp.PENDING_DOWNLOADS.append(user)
    await query.message.delete()
    SnowDev = await query.message.reply_text("**Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....**")

    for link in temp.QUEUE[user]:
        await queue_download(bot=bot, query=query, url=link)

    await query.message.reply_text(
        "𝗔𝗟𝗟 𝗟𝗜𝗡𝗞𝗦 𝗗𝗢𝗪𝗡𝗟𝗢𝗔𝗗𝗘𝗗 𝗦𝗨𝗖𝗖𝗘𝗦𝗦𝗙𝗨𝗟𝗟𝗬 ✅\n\n<b> 🍀 Developer </b> <a href=https://t.me/Snowball_official>ѕησωвαℓℓ ❄️</a>",
        reply_to_message_id=SnowDev.id,
        disable_web_page_preview=True,
    )

    temp.QUEUE.pop(user, None)
    temp.PENDING_DOWNLOADS.remove(user)


@Client.on_callback_query(filters.regex(r"^spankbang_playlist"))
async def handle_spankbang_playlist(bot: Client, query: CallbackQuery):
    user = query.from_user.id

    if user in temp.PENDING_DOWNLOADS:
        return await query.answer(
            f"Hᴇʏ {query.from_user.first_name},\nᴘʟᴀʏʟɪsᴛ ɪs ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ. Hᴀᴠᴇ ᴘᴀᴛɪᴇɴᴄᴇ ᴡʜɪʟᴇ ɪᴛ's ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ. 📥",
            show_alert=True,
        )

    temp.PENDING_DOWNLOADS.append(user)
    await query.message.delete()
    ms = await query.message.reply_text("**ᴘʟᴀʏʟɪsᴛ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ɪs sᴛᴀʀᴛᴇᴅ ✔**")

    for link in temp.PLAYLIST_DOWNLOAD.get(user, []):
        await queue_download(bot=bot, query=query, url=link)

    temp.PLAYLIST_DOWNLOAD.pop(user, None)
    await query.message.reply_text(
        "<b>ᴀʟʟ ᴠɪᴅᴇᴏs ᴏғ ᴛʜɪs ᴘʟᴀʏʟɪsᴛ ɪs ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ✅</b>\n\n<b> 🍀 Developer </b> <a href=https://t.me/Snowball_official>ѕησωвαℓℓ ❄️</a>",
        reply_to_message_id=ms.id,
        disable_web_page_preview=True,
    )


@Client.on_callback_query(filters.regex(r"^/dload"))
async def handle_video_quality(bot: Client, query: CallbackQuery):
    url = query.data
    defaultURL = query.message.reply_to_message.text

    await single_download(bot=bot, query=query, url=url, default_url=defaultURL)
    temp.PENDING_DOWNLOADS.remove(query.from_user.id)


@Client.on_callback_query(filters.regex(r"^download_file"))
async def handle_file(bot: Client, query: CallbackQuery):

    url = query.message.reply_to_message.text
    user = query.from_user.id

    if user in temp.PENDING_DOWNLOADS:
        return await query.answer(
            f"Hᴇʏ {query.from_user.first_name},\nDᴏᴡɴʟᴏᴀᴅ ɪs ᴀʟʀᴇᴀᴅʏ sᴛᴀʀᴛᴇᴅ ʜᴀᴠᴇ ᴘᴀᴛɪᴇɴᴄᴇ ᴡʜɪʟᴇ ɪᴛ's ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ. 📥",
            show_alert=True,
        )

    else:
        temp.PENDING_DOWNLOADS.append(user)

    if "eporner" in url:
        btn = []

        try:
            html_parser = requests.get(url)
            soup = BeautifulSoup(html_parser.text, "html5lib")
            download_links = soup.find("div", attrs={"class": "dloaddivcol"}).findAll(
                "a"
            )

            for link in download_links:
                btn.append(
                    [
                        InlineKeyboardButton(
                            text=link.text, callback_data=f"{link['href']}"
                        )
                    ]
                )

            await query.message.edit(
                "**sᴇʟᴇᴄᴛ ᴛʜᴇ ǫᴜᴀʟɪᴛʏ ᴏғ ᴠɪᴅᴇᴏ ?**",
                reply_markup=InlineKeyboardMarkup(btn),
            )
            return
        except Exception as e:
            return await query.message.edit(
                f"**sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ !!**\n\n**ERROR** : {e}"
            )

    await single_download(bot, query, url)
    temp.PENDING_DOWNLOADS.remove(user)


@Client.on_callback_query(filters.regex("^upgrade"))
async def handle_upgrade_callback(bot: Client, query: CallbackQuery):

    btn = [
        [InlineKeyboardButton("ᴘᴀʏ ᴛᴏ ᴀᴅᴍɪɴ", url="https://t.me/Snowball_Official")],
        [InlineKeyboardButton("ᴄʟᴏsᴇ ✘", callback_data="close")],
    ]
    markup = InlineKeyboardMarkup(btn)
    await query.message.edit(Txt.UPGRADE_MSG, reply_markup=markup)


@Client.on_message(filters.private & filters.command("cc"))
async def handle_clear_queue(bot: Client, message: Message):

    user = message.from_user.id

    if user in temp.QUEUE:
        temp.QUEUE.pop(user)
        if os.path.exists(f"downloads/{user}"):
            shutil.rmtree(f"downloads/{user}")

    if user in temp.TOKEN:
        temp.TOKEN.pop(user)
        if os.path.exists(f"downloads/{user}"):
            shutil.rmtree(f"downloads/{user}")

    if user in temp.PLAYLIST_DOWNLOAD:
        temp.PLAYLIST_DOWNLOAD.pop(user)
        if os.path.exists(f"downloads/{user}"):
            shutil.rmtree(f"downloads/{user}")

    if user in temp.PENDING_DOWNLOADS:
        temp.PENDING_DOWNLOADS.remove(user)
        if os.path.exists(f"downloads/{user}"):
            shutil.rmtree(f"downloads/{user}")

    await message.reply_text(
        "**ǫᴜᴇᴜᴇ ᴄʟᴇᴀʀᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ✅**", reply_to_message_id=message.id
    )
