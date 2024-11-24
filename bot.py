import asyncio
import logging
import warnings
import logging.config
from pyrogram import Client
from pyrogram.errors import FloodWait
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from config import Config
from aiohttp import web
from utility.database import db
from pytz import timezone
from datetime import datetime
from plugins.web_support import web_server

logging.config.fileConfig("logging.conf")
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pymongo").setLevel(logging.ERROR)


class Bot(Client):

    def __init__(self):
        super().__init__(
            name="AdultColonyBot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=15,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username
        if Config.WEBHOOK:
            app = web.AppRunner(await web_server())
            await app.setup()
            bind_address = "0.0.0.0"
            await web.TCPSite(app, bind_address, Config.PORT).start()
        logging.info(f"{me.first_name} ✅✅ BOT started successfully ✅✅")

        if Config.LOG_CHANNEL:
            try:
                curr = datetime.now(timezone("Asia/Kolkata"))
                date = curr.strftime("%d %B, %Y")
                time = curr.strftime("%I:%M:%S %p")
                await self.send_message(
                    Config.LOG_CHANNEL,
                    f"**__{me.mention} Iꜱ Rᴇsᴛᴀʀᴛᴇᴅ !!**\n\n📅 Dᴀᴛᴇ : `{date}`\n⏰ Tɪᴍᴇ : `{time}`\n🌐 Tɪᴍᴇᴢᴏɴᴇ : `Asia/Kolkata`\n\n🉐 Vᴇʀsɪᴏɴ : `v{__version__} (Layer {layer})`</b>",
                )
            except:
                print("Pʟᴇᴀꜱᴇ Mᴀᴋᴇ Tʜɪꜱ Iꜱ Aᴅᴍɪɴ Iɴ Yᴏᴜʀ Lᴏɢ Cʜᴀɴɴᴇʟ")

        success = failed = 0
        users = await db.get_all_users()
        async for user in users:
            chat_id = user["id"]
            try:
                await self.send_message(
                    chat_id=chat_id, text="**๏[-ิ_•ิ]๏ bot restarted !**"
                )
                success += 1

            except FloodWait as e:
                await asyncio.sleep(e.value + 1)
                await self.send_message(
                    chat_id=chat_id, text="**๏[-ิ_•ิ]๏ bot restarted !**"
                )
                success += 1
            except Exception:
                failed += 1

    async def stop(self, *args):
        await super().stop()
        logging.info("Bot Stopped 🙄")


bot = Bot()
bot.run()