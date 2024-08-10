from datetime import timedelta, datetime
import random
from pyrogram import Client, filters
from pyrogram.types import *
from config import Config
from helper.utils import str_to_b64
from uuid import uuid4

from plugins.down_and_up import fetch_shorturl

@Client.on_message(filters.private & filters.command('gentoken'))
async def genToken(client: Client, message: Message):
    
    if message.from_user.id in Config.ADMIN:
        return await message.reply_text("> ** You Don't Need To Generate Token You're Admin ‼️ **", reply_to_message_id=message.id)
    
    # Generate a random expiration time in hours
    hours_valid = random.randint(5, 24)
    
    encrypt_info = str_to_b64("{}:{}:{}".format(message.from_user.id, hours_valid, uuid4().hex))
    shorturl = f"{Config.SHORTENER_API}https://t.me/{Config.BOT_USERNAME}?start={encrypt_info}&format=text"
    print(shorturl)
    url = await fetch_shorturl(shorturl=shorturl)
    btn =  InlineKeyboardMarkup([[InlineKeyboardButton('💫 ɢᴇɴᴇʀᴀᴛᴇ ᴛᴏᴋᴇɴ 💫', url=url)]])
    
    await message.reply_text("> ** 💫 Generate a token to get ultimate access to AdultColony. The token's expiration time will be chosen randomly, so it's up to your luck how long you will have access. 💫 **", reply_markup=btn,)
    