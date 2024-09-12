import random
from pyrogram import Client, filters
from helper.database import db
from helper.utils import str_to_b64
from plugins.down_and_up import fetch_shorturl
from pyrogram.types import *
from config import Config, temp
from uuid import uuid4


@Client.on_message(filters.command("random"))
async def get_random_videos(client: Client, message: Message):
    
    user_status = await db.get_user_status(message.from_user.id)

    if user_status["plan"] == "free" and int(message.from_user.id) not in Config.ADMIN:
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
    
    files = await db.get_all_files()
    
    randomPick = random.choice(files)
    
    dc = await message.reply_text("**Please Wait...**")
    await client.copy_message(message.chat.id ,int(Config.DUMP_VIDEOS), int(randomPick["msg_id"]))
    await dc.delete()