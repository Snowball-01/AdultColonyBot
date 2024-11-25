import os
import re
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from utility import spankbang_playlist_fetch, filter_spankbang_playlist, str_to_b64
from uuid import uuid4
from config import temp
from utility.hentaifox import convert_images_to_pdf
import aiohttp
from config import Config
from utility.database import db
from utility import fetch_shorturl


regex_search = r"(?:https?:\/\/)?(?:www\.)?(?:spankbang|fullxcinema|pornhub|xnxx|xvideos|japanhdv\.com|javhd\.today|javhd\.icu|javtsunami\.com|javgiga.com|japteenx\.com|kissjav\.com|xhamster|hentaifox\.com|eporner\.com)"


@Client.on_message(filters.private & filters.regex(regex_search))
async def handle_option(bot: Client, message: Message):

    user_status = await db.get_user_status(message.from_user.id)

    if user_status["plan"] == "free" and int(message.from_user.id) not in Config.ADMIN and Config.SHORTENER_API:
        token = await db.get_token(message.from_user.id)
        if not token:
            tokenid = uuid4().hex[:16]
            temp.TOKEN_VERIFY.append(tokenid)
            uuid = f"verify_{str_to_b64(tokenid)}"
            shorturl = f"{Config.SHORTENER_API}https://t.me/{Config.BOT_USERNAME}?start={uuid}&format=text"
            url = await fetch_shorturl(shorturl=shorturl)
            btn = InlineKeyboardMarkup(
                [[InlineKeyboardButton("💫 Click Here 💫", url=url)]]
            )
            return await message.reply_text(
                "**Your Ads token is expired, refresh your token and try again.**\n\n> **Token Timeout: 1day**\n\n **🤔 What is the token ?**\n\n> **This is an ads token. If you pass 1 ad, you can use the bot for 24 Hour after passing the ad.**",
                reply_markup=btn,
            )

    if "hentaifox.com" in message.text:

        if message.from_user.id in temp.IN_QUEUE_DOWNLOADS:
            return await message.reply_text(
                "**☘️ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ᴡʜɪʟᴇ ᴘʀᴇᴠɪᴏᴜs ᴏɴᴇ ɪs ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...**",
                reply_to_message_id=message.id,
            )

        else:
            temp.IN_QUEUE_DOWNLOADS.append(message.from_user.id)

        process = await message.reply_sticker(
            "CAACAgUAAxkBAAEL6lNmHNWZGZ_A0e2WEqxDcrDILHOZ9wACpwADyJRkFGCmdrVn5RydNAQ",
            reply_to_message_id=message.id,
        )
        os.makedirs(f"downloads/{message.from_user.id}", exist_ok=True)

        manga_id = re.search(r"\d+", message.text).group()
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{Config.API}/hentaifox/get?book={manga_id}"
            ) as resp:
                response = await resp.json()
                data = response["data"]
                images_list = data["image"]
                title = data["title"]
                source = response["source"]

        await convert_images_to_pdf(
            image_urls=images_list,
            bot=bot,
            message=message,
            source=source,
            title=title,
            process=process,
        )
        return

    elif "spankbang.party" in message.text and "playlist" in message.text:
        ms = await message.reply_text(
            "**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...**", reply_to_message_id=message.id
        )
        new_url = await filter_spankbang_playlist(message.text)
        status = await spankbang_playlist_fetch(new_url, message.from_user.id)

        if status == 1:

            btn = [
                [
                    InlineKeyboardButton("ʏᴇs", callback_data="spankbang_playlist"),
                    InlineKeyboardButton("ɴᴏ", callback_data="close"),
                ]
            ]
            text = f"**☘️ ᴛʜɪs ɪs ᴀ ᴘʟᴀʏʟɪsᴛ ғʀᴏᴍ sᴘᴀɴᴋʙᴀɴɢ sɪᴛᴇ ᴛᴏᴛᴀʟ __`{len(temp.PLAYLIST_DOWNLOAD.get(message.from_user.id))}`__ ᴠɪᴅᴇᴏs ғᴏᴜɴᴅ ɪɴ ᴛʜɪs ᴘʟᴀʏʟɪsᴛ**\n\n**ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴀʟʟ ᴛʜᴇ ᴠɪᴅᴇᴏs ᴏғ ᴛʜɪs ᴘʟᴀʏʟɪsᴛ ?**"

            return await ms.edit(text, reply_markup=InlineKeyboardMarkup(btn))
        else:
            return await ms.edit("**sᴏᴍᴇᴛʜɪɴɢs ᴡᴇɴᴛ ᴡʀᴏɴɢ** ❗")

    btn = [
        [InlineKeyboardButton("🔻 ᴅᴏᴡɴʟᴏᴀᴅ 🔻", callback_data=f"download_file")],
        [
            InlineKeyboardButton("➕ ᴀᴅᴅ ǫᴜᴇᴜᴇ ➕", callback_data=f"add_queue"),
            InlineKeyboardButton("✔ ᴅᴏɴᴇ ✔", callback_data=f"done_queue"),
        ],
        [InlineKeyboardButton("✘ ᴄʟᴏsᴇ ✘", callback_data="close")],
    ]
    ms = await message.reply_text(
        "**Do you want to download this file ?**",
        reply_markup=InlineKeyboardMarkup(btn),
        reply_to_message_id=message.id,
    )
