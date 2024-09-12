import random
from pyrogram import Client, filters
from helper.database import db
from pyrogram.types import *
from config import Config


@Client.on_message(filters.command("random"))
async def get_random_videos(client: Client, message: Message):
    
    files = await db.get_all_files()
    
    randomPick = random.choice(files)

    await client.copy_message(message.chat.id ,int(Config.DUMP_VIDEOS), int(randomPick["msg_id"]))