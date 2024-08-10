from datetime import datetime, timedelta
import sys
from config import Config, temp
from helper.database import Database
from helper.utils import is_plan_expire

db = Database(Config.DB_URL, Config.BOT_USERNAME)


async def handle_user_status(bot, cmd):
    chat_id = cmd.from_user.id
    ban_status = await db.get_ban_status(chat_id)
    if ban_status["is_banned"]:
        if (
            datetime.date.today() - datetime.date.fromisoformat(ban_status["banned_on"])
        ).days > ban_status["ban_duration"]:
            await db.remove_ban(chat_id)
        else:
            await cmd.reply_text(
                "You R Banned!.. Contact @SnowBall_Official 😝", quote=True
            )
            return


async def handle_plan_expire(bot, cmd):
    chat_id = cmd.from_user.id

    user_status = await db.get_user_status(chat_id)
    user_plan_expire_on = user_status["plan_expire_on"]
    if user_status["plan"] == "premium" and is_plan_expire(user_plan_expire_on):
        await db.remove_premium(chat_id)
        await cmd.reply_text(
            f"Hᴇʏ, {cmd.from_user.mention}\n\n**Yᴏᴜʀ ᴘʟᴀɴ ɪs ᴇxᴘɪʀᴇᴅ ᴘʟᴇᴀsᴇ ᴜᴘᴅᴀᴛᴇ ʏᴏᴜʀ ᴘʟᴀɴ ᴛᴏ ɢᴇᴛ ᴀᴄᴄᴇss ᴏғ ᴀʟʟ ᴛʜᴇ ғᴇᴀᴛᴜʀᴇs ☹️**"
        )


async def handle_token_expire(bot, cmd):

    chat_id = cmd.from_user.id

    if chat_id in temp.TOKEN:
        # Convert the string to a datetime object
        user_token_time = temp.TOKEN[chat_id]
        print(user_token_time)
        date_obj = datetime.strptime(user_token_time, "%Y-%m-%d %H:%M:%S")

        # Get the current datetime
        current_datetime = datetime.strptime(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S"
        )

        if current_datetime > date_obj:
            temp.TOKEN.pop(chat_id)
            await cmd.reply_text("> ⚠️ ** Token Expired. Please Generate New Token By Using /gentoken **")
            return

    await cmd.continue_propagation()
