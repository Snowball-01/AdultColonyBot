import random
import re
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
from helper.database import db
from helper.utils import humanbytes, b64_to_str
from datetime import timedelta, datetime
import time

logger = logging.getLogger(__name__)


@Client.on_message(filters.private & filters.command("start"))
async def start(client: Client, message: Message):

    if message.command[0] == "start" and len(message.command) == 2:
        if not message.command[1].startswith(Config.BOT_USERNAME):
            decrypt = b64_to_str(message.command[1]).split(":")
            token = await db.get_token(decrypt[2])
            if token:
                return await message.reply_text(
                    f"> ** Token Already Redeemed By - ** `{token['username']}`\n\n** 💫 Generate Different Token Use /gentoken **",
                    reply_to_message_id=message.id,
                )
            if int(decrypt[0]) == message.from_user.id:
                # Calculate expiration datetime
                expiration_time = datetime.now() + timedelta(hours=int(decrypt[1]))

                if int(decrypt[0]) not in temp.TOKEN:
                    temp.TOKEN[int(decrypt[0])] = expiration_time.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    await message.reply_text(
                        f"** Token Generated Successfully ✅ **\n\n> ** Token Expiration Time: ** `{expiration_time.strftime('%Y-%m-%d %H:%M:%S')}`",
                        reply_to_message_id=message.id,
                    )
                    await db.add_token(decrypt[2], message.from_user.first_name)
                return
            else:
                return await message.reply_text(
                    "> ** You Can't Redeem Other's Token **\n\n** 💫 Generate Different Token Use /gentoken ** ❄️",
                    reply_to_message_id=message.id,
                )

        else:
            message_id = b64_to_str(message.command[1].split("_")[1])
            try:
                return await client.copy_message(
                    chat_id=message.from_user.id,
                    from_chat_id=Config.DUMP_VIDEOS,
                    message_id=int(message_id),
                )
            except:
                return await message.reply_text(
                    "**ғɪʟᴇ ɪs ᴅᴇʟᴇᴛᴇᴅ ʙʏ ᴀᴅᴍɪɴ** ❄️", reply_to_message_id=message.id
                )

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
            [InlineKeyboardButton("🌐 ᴡᴇʙsɪᴛᴇs", callback_data="websites")],
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
                    [InlineKeyboardButton("🍣 ᴊᴀᴘᴀɴᴇsᴇ", callback_data="jap")],
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

    elif data == "jap":
        await query.message.edit_media(
            InputMediaPhoto(random.choice(Config.PICS), Txt.JAP_TXT),
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("• ʙᴀᴄᴋ", callback_data="websites")],
                    [
                        InlineKeyboardButton(
                            "ᴊᴀᴘᴀɴ ʜᴅᴠ", switch_inline_query_current_chat="@JapanHdv"
                        ),
                        InlineKeyboardButton(
                            "ᴊᴀᴘᴛᴇᴇɴ x", switch_inline_query_current_chat="@Japteenx"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "ᴋɪssᴊᴀᴠ", switch_inline_query_current_chat="@KissJav"
                        ),
                        InlineKeyboardButton(
                            "ᴊᴀᴠʜᴅ ᴛᴏᴅᴀʏ",
                            switch_inline_query_current_chat="@JavHdToday",
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "ᴊᴀᴠʜᴅ ᴛsᴜɴᴀᴍɪ",
                            switch_inline_query_current_chat="@JavTsunami",
                        ),
                        InlineKeyboardButton(
                            "ᴊᴀᴠʜᴅ ɢɪɢᴀ",
                            switch_inline_query_current_chat="@JavGiga",
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
