import re
import os
import time

id_pattern = re.compile(r'^.\d+$')


class Config(object):
     # pyro client config
    API_ID = os.environ.get("API_ID", "27060846")  # ⚠️ Required
    API_HASH = os.environ.get("API_HASH", "8f39072a61dbb296f38e4ff2b6cbe478")  # ⚠️ Required
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7040879932:AAHLhmS8TCsCJBQLC44S507RRnKsIMgZVmM")  # ⚠️ Required
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "AdultColonyBot")  # ⚠️ Required

    # database config
    DB_URL = os.environ.get("DB_URL", "mongodb+srv://ADULTCOLONY:ADULTCOLONY@cluster0.x53fa1k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  # ⚠️ Required


    # other configs
    BOT_UPTIME = time.time()
    PICS = os.environ.get("PICS", "https://telegra.ph/file/71b9adb9c7cfa113c1be2.jpg https://telegra.ph/file/2b7fc62babf78aaf48994.jpg https://telegra.ph/file/3b1f1f818ba7c63b2396a.jpg https://telegra.ph/file/a40e4288a2df067cb516d.jpg https://telegra.ph/file/32ed04bb906ccd6b1e3fc.jpg https://telegra.ph/file/e62961e581d207e2911c8.jpg https://telegra.ph/file/f4a80205d3c0a52dc3bb3.jpg https://telegra.ph/file/e56fd115fc8c768adeea6.jpg https://telegra.ph/file/be47d365473708a878ce7.jpg https://telegra.ph/file/885998feda9b6f702e35f.jpg https://telegra.ph/file/395ca8d46028a6c411ceb.jpg https://telegra.ph/file/b510f0bc05e6b2c4c932f.jpg https://telegra.ph/file/08b86c83bd968bc3cd8ef.jpg https://telegra.ph/file/5ab87ac08a127f007b697.jpg https://telegra.ph/file/e85aa9dd3be75de1116c5.jpg https://telegra.ph/file/c61bc2d79d2de5ee77e90.jpg https://telegra.ph/file/f5ddae173b250232e029a.jpg https://telegra.ph/file/5aad41a371a9ef1724d64.jpg https://telegra.ph/file/ab26ba51fee9c108bfff9.jpg https://telegra.ph/file/a5065bac7ff30a79084dc.jpg https://telegra.ph/file/73834c98dc278e795cebe.jpg https://telegra.ph/file/2c00c86a249c1decc3dc0.jpg").split()
    ADMIN = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '6065594762').split()]  # ⚠️ Required
    FORCE_SUB = os.environ.get('FORCE_SUB', 'SnowDevs')  # ⚠️ Required without [@]
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001971176803"))  # ⚠️ Required
    SHORTENER_API = os.environ.get("SHORTENER_API", "") # ⚠️ SHOULD BE LIKE THIS "https://runurl.in/api?api=d0e0909f2c1e5f1130e4b643cdba7e39a28341eb&url="
    DUMP_VIDEOS = int(os.environ.get("DUMP_VIDEOS", "-1002129817205")) # ⚠️ Required
    API = os.environ.get("API", "http://82.180.131.185:3000") # ⚠️ Must not ends with '/'

    # wes response configuration
    WEBHOOK = bool(os.environ.get("WEBHOOK", False))
    PORT = int(os.environ.get("PORT", "8080"))


class Txt(object):
    # part of text configuration
    START_TXT = """<b>Hello {} 👋,
━━━━━━━━━━━━━━━━━━━━━
** Tʜɪs Bᴏᴛ Cᴀɴ Sᴇᴀʀᴄʜ Vɪᴅᴇᴏs Tʜʀᴏᴜɢʜ Aᴅᴜʟᴛ Sɪᴛᴇs & Dᴏᴡɴʟᴏᴀᴅ Tʜᴇᴍ Fᴏʀ Yᴏᴜ **
━━━━━━━━━━━━━━━━━━━━━
> ⚠️Tʜᴇ Bᴏᴛ Cᴏɴᴛᴀɪɴs 18+ Cᴏɴᴛᴇɴᴛ Sᴏ Kɪɴᴅʟʏ Aᴄᴄᴇss ɪᴛ ᴡɪᴛʜ Yᴏᴜʀ ᴏᴡɴ Rɪsᴋ. Cʜɪʟᴅʀᴇɴ Pʟᴇᴀsᴇ Sᴛᴀʏ Aᴡᴀʏ." Wᴇ ᴅᴏɴ'ᴛ ɪɴᴛᴇɴᴅ ᴛᴏ sᴘʀᴇᴀᴅ Pøʀɴᴏ- -ɢʀᴀᴘʜʏ ʜᴇʀᴇ. Iᴛ's ᴊᴜsᴛ ᴀ ʙᴏᴛ ғᴏʀ ᴀ" ᴘᴜʀᴘᴏsᴇ ᴀs ᴍᴀɴʏ ᴏғ ᴛʜᴇᴍ ᴡᴀɴᴛᴇᴅ."
━━━━━━━━━━━━━━━━━━━━━
** Cʟɪᴄᴋ Tʜᴇ Bᴜᴛᴛᴏɴs Bᴇʟᴏᴡ Tᴏ Exᴘʟᴏʀᴇ **
"""

    ABOUT_TXT = """<b>
➥ ᴍy ɴᴀᴍᴇ : {}
➥ Pʀᴏɢʀᴀᴍᴇʀ : <a href=https://t.me/Snowball_Official>ѕησωвαℓℓ ❄️</a> 
➥ ꜰᴏᴜɴᴅᴇʀ ᴏꜰ : <a href=https://t.me/Kdramaland>K-Lᴀɴᴅ</a>
➥ Lɪʙʀᴀʀy : <a href=https://github.com/pyrogram>Pyʀᴏɢʀᴀᴍ</a>
➥ Lᴀɴɢᴜᴀɢᴇ: <a href=https://www.python.org>Pyᴛʜᴏɴ 3</a>
➥ Dᴀᴛᴀ Bᴀꜱᴇ: <a href=https://cloud.mongodb.com>Mᴏɴɢᴏ DB</a>
➥ ᴍʏ ꜱᴇʀᴠᴇʀ : <a href=https://dashboard.heroku.com>Heroku</a>
➥ ᴠᴇʀsɪᴏɴ : v2.6.0
"""

    DONATE = "<b>Your generous donation, no matter the amount, is sincerely appreciated and will greatly support our bot's development.</b>\n\n<b>UPI ID -</b> <code>ritesh.r8@paytm</code>"

    HELP_TXT = """
**🌐 Tʜᴇ ʙᴏᴛ ᴡɪʟʟ ʜᴇʟᴘ ʏᴏᴜ ᴅᴏᴡɴʟᴏᴀᴅ ғɪʟᴇs ᴜsɪɴɢ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʟɪɴᴋs. **

💫 PornHub
💫 Xnxx
💫 Xvideos
💫 Xhamster
💫 SpankBang
💫 JapanHdv
💫 JapTeenx
💫 KissJav
💫 JavHdToday
💫 JavTsunami
💫 JavGiga
💫 Hentaifox

❗ Dᴇᴠᴇʟᴏᴘᴇʀ :- <a href=https://t.me/Snowball_official>ѕησωвαℓℓ ❄️</a>
"""

    WEBSITES_TXT = """
Tʜɪs ʙᴏᴛ ᴄᴀɴ ᴅᴏᴡɴʟᴏᴀᴅ ғɪʟᴇs ᴠᴀʀɪᴏᴜs ᴘᴏʀɴ sɪᴛᴇs.

✿ Hᴏᴡ ᴛᴏ sᴇᴀʀᴄʜ ?

➜ `@AdultColonyBot @Xhamster Russian 1`

** ᴀs ʏᴏᴜ sᴇᴇɴ ғʀᴏᴍ ᴀʙᴏᴠᴇ ᴛᴇxᴛ `@AdultColonyBot @Xhamster Russian 1` ɪᴛ ᴍᴇᴀɴs ᴛʜᴇ ʙᴏᴛ ᴡɪʟʟ sᴇᴀʀᴄʜ ғᴏʀ Rᴜssɪᴀɴ ᴠɪᴅᴇᴏs ғʀᴏᴍ ᴛʜᴇ xʜᴀᴍsᴛᴇʀ sɪᴛᴇ ᴏɴ ᴘᴀɢᴇ ɴᴜᴍʙᴇʀ 1 ᴀɴᴅ sᴏ ᴀɴᴅ sᴏ ғᴏʀᴛʜ **
"""

    JAP_TXT = """
**ʜᴇʀᴇ ʏᴏᴜ'ʟʟ ᴏɴʟʏ ғɪɴᴅ ᴀsɪᴀɴ ʀᴇʟᴀᴛᴇᴅ ᴄᴏɴᴛᴇɴᴛ ʟɪᴋᴇ ᴊᴀᴘᴀɴᴇsᴇ, ᴋᴏʀᴇᴀɴ, ᴄʜɪɴᴇsᴇ, ᴛʜᴀɪ ᴇᴛᴄ...**
"""

    STATS_TXT = """
╔════❰ sᴇʀᴠᴇʀ sᴛᴀᴛs  ❱═❍⊱❁۪۪
║╭━━━━━━━━━━━━━━━➣
║┣⪼ ᴜᴩᴛɪᴍᴇ: `{0}`
║┣⪼ ᴛᴏᴛᴀʟ sᴘᴀᴄᴇ: `{1}`
║┣⪼ ᴜsᴇᴅ: `{2} ({3}%)`
║┣⪼ ꜰʀᴇᴇ: `{4}`
║┣⪼ ᴄᴘᴜ: `{5}%`
║┣⪼ ʀᴀᴍ: `{6}%`
║╰━━━━━━━━━━━━━━━➣
╚══════════════════❍⊱❁۪۪        
"""

    PROGRESS_BAR = """<b>\n
╭━━━━❰ᴘʀᴏɢʀᴇss ʙᴀʀ❱━➣
┣⪼ 🗃️ Sɪᴢᴇ: {1} | {2}
┣⪼ ⏳️ Dᴏɴᴇ : {0}%
┣⪼ 🚀 Sᴩᴇᴇᴅ: {3}/s
┣⪼ ⏰️ Eᴛᴀ: {4}
╰━━━━━━━━━━━━━━━➣ </b>"""

    UPGRADE_MSG = """
💸 ᴡʜᴀᴛ ʏᴏᴜ'ʟʟ ɢᴇᴛ ɪғ ʏᴏᴜ'ʀᴇ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀ ? 

💠 **Nᴏ ʀᴇsᴛʀɪᴄᴛɪᴏɴ**
💠 **Aᴄᴄᴇss ᴛᴏ ᴀʟʟ sɪᴛᴇs**
💠 **4ɢ ᴅᴏᴡɴʟᴏᴀᴅs**
💠 **Cᴀɴ ᴅᴏᴡɴʟᴏᴀᴅ ᴘʟᴀʏʟɪsᴛ ᴏғ sᴘᴀɴᴋʙᴀɴɢ**
💠 **Yᴏᴜʀ ᴅᴇsɪʀᴇ ᴡᴇʙsɪᴛᴇ ᴡɪʟʟ ʙᴇ ᴀᴅᴅᴇᴅ ᴛᴏ ʙᴏᴛ ɪғ ᴘᴏssɪʙʟᴇ ᴀs ᴘᴇʀ ʀᴇǫᴜᴇsᴛ**

☛ Pʀɪᴄᴇ : ₹100/month or $1.20/month

**sᴏ ᴡʜᴀᴛ ʏᴏᴜ'ʀᴇ ᴡᴀɪᴛɪɴɢ ғᴏʀ ᴜᴘɢʀᴀᴅᴇ ɴᴏᴡ 🔥**

> 🇮🇳 UPI ID : `riteshraushan30@oksbi`

💸 ᴄʀʏᴘᴛᴏ ᴏᴘᴛɪᴏɴs 💸

> USDT : `TRwy6i7kiqT5aEJgjvsELJqjS226w4ivJ6`
> BIT COIN : `16S5fouShzfRY92GrX9Q7J2fQXYTpoiNBn`
> TON COIN : `UQAQfW0t7njYDDjif_wWGA7j0jpuGNnBo-9TrAzed2eQz8ha`
"""

    YOU_ARE_ADMIN_TEXT = """
Hᴇʏ {},

**Yᴏᴜ ᴀʀᴇ ᴀᴅᴍɪɴ ʏᴏᴜ ᴅᴏɴ'ᴛ ɴᴇᴇᴅ ᴘʀᴇᴍɪᴜᴍ ʏᴏᴜ ᴄᴀɴ ᴀᴄᴄᴇss ᴀʟʟ ᴛʜᴇ ғᴇᴀᴛᴜʀᴇs 👑**
"""

class temp(object):
    
    QUEUE = {}
    PENDING_DOWNLOADS = []
    PLAYLIST_DOWNLOAD = {}
    TOKEN = {}
