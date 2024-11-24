import random
import shutil
import psutil
from pyrogram import Client, filters
import logging
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    CallbackQuery,
    InputMediaPhoto,
)
from config import Config, Txt, temp
from utility.database import db
from utility import b64_to_str, humanbytes
import time

logger = logging.getLogger(__name__)


@Client.on_message(filters.private & filters.command("start"))
async def start(client: Client, message: Message):

    if message.command[0] == "start" and len(message.command) == 2:
        if message.command[1].startswith("verify"):
            user_token = b64_to_str(message.command[1].split("_")[1])
            if user_token in temp.TOKEN_VERIFY:
                await message.reply_text(
                    "> **Your token successfully verified and valid for: 24 Hour**",
                    reply_to_message_id=message.id,
                )
                await db.add_token(message.from_user.id)
                temp.TOKEN_VERIFY.remove(user_token)
                return
            else:
                await message.reply_text(
                    "> **Your token is invalid or Expired** ‼️", reply_to_message_id=message.id
                )
                return

        message_id = b64_to_str(message.command[1].split("_")[1])
        try:
            return await client.copy_message(
                chat_id=message.from_user.id,
                from_chat_id=Config.DUMP_VIDEOS,
                message_id=int(message_id),
            )
        except:
            return

    user = message.from_user
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⛅ ᴜᴘᴅᴀᴛᴇs", url="https://t.me/Kdramaland"),
                InlineKeyboardButton("🌨️ sᴜᴘᴘᴏʀᴛ", url="https://t.me/SnowDevs"),
            ],
            [
                InlineKeyboardButton("• ᴀʙᴏᴜᴛ", callback_data="about"),
                InlineKeyboardButton("• ʜᴇʟᴘ", callback_data="help"),
            ],
            [InlineKeyboardButton("🌏 ᴡᴇʙsɪᴛᴇs", callback_data="websites")],
        ]
    )

    await message.reply_photo(
        random.choice(Config.PICS),
        caption=Txt.START_TXT.format(user.mention),
        reply_markup=button,
    )


@Client.on_message(filters.private & filters.command("donate"))
async def func_donate(client, message):
    user = message.from_user
    buttons = [
        [
            InlineKeyboardButton("❄️ ѕησωвαℓℓ", url="https://t.me/Snowball_Official"),
            InlineKeyboardButton("✘ ᴄʟᴏsᴇ", callback_data="close"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_message(
        chat_id=user.id, text=Txt.DONATE, reply_markup=reply_markup
    )


# ⚠️ Handling CallBack Query⚠️


@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data
    if data == "start":
        await query.message.edit_media(
            InputMediaPhoto(
                random.choice(Config.PICS),
                Txt.START_TXT.format(query.from_user.mention),
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "⛅ Uᴩᴅᴀᴛᴇꜱ", url="https://t.me/Kdramaland"
                        ),
                        InlineKeyboardButton("🌨️ Sᴜᴩᴩᴏʀᴛ", url="https://t.me/SnowDevs"),
                    ],
                    [
                        InlineKeyboardButton("• ᴀʙᴏᴜᴛ", callback_data="about"),
                        InlineKeyboardButton("• ʜᴇʟᴘ", callback_data="help"),
                    ],
                    [InlineKeyboardButton("🌐 ᴡᴇʙsɪᴛᴇs", callback_data="websites")],
                ]
            ),
        )

    elif data == "websites":
        await query.message.edit_media(
            InputMediaPhoto(random.choice(Config.PICS), Txt.WEBSITES_TXT),
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("• ʙᴀᴄᴋ", callback_data="start")],
                    [
                        InlineKeyboardButton(
                            "xɴxx", switch_inline_query_current_chat="@Xnxx"
                        ),
                        InlineKeyboardButton(
                            "xᴠɪᴅᴇᴏs", switch_inline_query_current_chat="@Xvideos"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "sᴘᴀɴᴋʙᴀɴɢ", switch_inline_query_current_chat="@SpankBang"
                        ),
                        InlineKeyboardButton(
                            "xʜᴀᴍsᴛᴇʀ", switch_inline_query_current_chat="@Xhamster"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "ᴘᴏʀɴ ʜᴜʙ", switch_inline_query_current_chat=""
                        ),
                        InlineKeyboardButton(
                            "ᴇᴘᴏʀɴᴇʀ", switch_inline_query_current_chat="@Eporner"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "ʜᴇɴᴛᴀɪ ғᴏx", switch_inline_query_current_chat="@HentaiFox"
                        )
                    ],
                ]
            ),
        )

    elif data == "help":

        await query.message.edit_media(
            InputMediaPhoto(random.choice(Config.PICS), Txt.HELP_TXT),
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("• sᴇʀᴠᴇʀ sᴛᴀᴛs", callback_data="stats")],
                    [
                        InlineKeyboardButton("• ʙᴀᴄᴋ", callback_data="start"),
                        InlineKeyboardButton("✘ ᴄʟᴏsᴇ", callback_data="close"),
                    ],
                ]
            ),
        )

    elif data == "about":
        await query.message.edit_media(
            InputMediaPhoto(
                random.choice(Config.PICS), Txt.ABOUT_TXT.format(client.mention)
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("• ʙᴀᴄᴋ", callback_data="start"),
                        InlineKeyboardButton("✘ ᴄʟᴏsᴇ", callback_data="close"),
                    ]
                ]
            ),
        )

    elif data == "stats":
        buttons = [
            [
                InlineKeyboardButton("• ʙᴀᴄᴋ", callback_data="help"),
                InlineKeyboardButton("⟲ ʀᴇʟᴏᴀᴅ", callback_data="stats"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        currentTime = time.strftime(
            "%Hh%Mm%Ss", time.gmtime(time.time() - Config.BOT_UPTIME)
        )
        total, used, free = shutil.disk_usage(".")
        total = humanbytes(total)
        used = humanbytes(used)
        free = humanbytes(free)
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage("/").percent
        await query.message.edit_media(
            InputMediaPhoto(
                random.choice(Config.PICS),
                Txt.STATS_TXT.format(
                    currentTime, total, used, disk_usage, free, cpu_usage, ram_usage
                ),
            ),
            reply_markup=reply_markup,
        )

    elif data == "userbot":
        userBot = await db.get_user_bot(query.from_user.id)

        text = f"Name: {userBot['name']}\nUserName: @{userBot['username']}\n UserId: {userBot['user_id']}"

        await query.message.edit(
            text=text,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("❌ ʀᴇᴍᴏᴠᴇ ❌", callback_data="rmuserbot")],
                    [InlineKeyboardButton("✘ ᴄʟᴏsᴇ ✘", callback_data="close")],
                ]
            ),
        )

    elif data == "rmuserbot":
        try:
            await db.remove_user_bot(query.from_user.id)
            await query.message.edit(
                text="**User Bot Removed Successfully ✅**",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("✘ ᴄʟᴏsᴇ ✘", callback_data="close")]]
                ),
            )
        except:
            await query.answer(
                f"Hey {query.from_user.first_name}\n\n You have already deleted the user"
            )

    elif data == "close":
        user = query.from_user.id
        try:
            if user in temp.PLAYLIST_DOWNLOAD:
                temp.PLAYLIST_DOWNLOAD.pop(user)

            await query.message.delete()
            await query.message.reply_to_message.delete()
            await query.message.continue_propagation()
        except:
            await query.message.delete()
            await query.message.continue_propagation()
