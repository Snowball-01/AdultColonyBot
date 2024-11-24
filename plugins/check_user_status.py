from datetime import datetime
from config import Config
from utility.database import Database
from utility import is_plan_expire, is_token_expired

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
    
    user_status = await db.get_user_status(chat_id)
    if user_status["plan"] == "free" and int(chat_id) not in Config.ADMIN and Config.SHORTENER_API:
        token_expire_on = await db.get_token(chat_id)
        if token_expire_on and is_token_expired(token_expire_on):
            await db.remove_token(chat_id)
    
    await cmd.continue_propagation()
