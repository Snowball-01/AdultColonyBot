import asyncio
from base64 import standard_b64decode, standard_b64encode
from datetime import datetime
import math
from queue import Queue
import sys
from bs4 import BeautifulSoup
from pyrogram.types import CallbackQuery
import re
import time
import aiofiles
import aiohttp
from pyrogram import Client
from PIL import Image
from pytz import timezone
from config import Config, temp
from config import Txt
from utility.eporner import get_eporner_video_info
from utility.pronhub import get_pornhub_video_info
from utility.spankbang import get_spankbang_video_info
from utility.xhamster import get_xhamster_video_info
from utility.xnxx import get_xnxx_video_info
from utility.xvideos import get_xvideos_video_info


async def download_thumbnail(thumbnail_url, thumbnail_filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail_url) as response:
            if response.status == 200:
                async with aiofiles.open(thumbnail_filename, "wb") as f:
                    await f.write(await response.read())

async def animated_loading(query:CallbackQuery, text:str):
    loading_stages = ['|', '/', '-', '\\']
    for stage in loading_stages:
        await query.message.edit(f"{text} {stage}")
        await asyncio.sleep(0.2)

async def getVideoInfo(link: str) -> object:
    if "eporner" in link:
        return await get_eporner_video_info(link)
    elif "pornhub" in link:
        return await get_pornhub_video_info(link)
    elif "spankbang" in link:
        return await get_spankbang_video_info(link)
    elif "xhamster" in link:
        return await get_xhamster_video_info(link)
    elif "xnxx" in link:
        return await get_xnxx_video_info(link)
    elif "xvideos" in link:
        return await get_xvideos_video_info(link)
    
    else:
        return {}
    

# Check if videoInfo is already in QUEUE
def is_video_in_queue(queue, user, video_info):
    user_queue = queue.get(user, [])
    return video_info in user_queue


def humanbytes(size):
    if not size:
        return ""
    power = 2**10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


async def progress_for_pyrogram(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start
    if round(diff % 5.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "{0}{1}".format(
            "".join(["⬢" for i in range(math.floor(percentage / 5))]),
            "".join(["⬡" for i in range(20 - math.floor(percentage / 5))]),
        )
        tmp = progress + Txt.PROGRESS_BAR.format(
            round(percentage, 2),
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            estimated_total_time if estimated_total_time != "" else "0 s",
        )
        try:
            await message.edit(text=f"{ud_type}\n\n{tmp}")
        except:
            pass


async def fetch_page(session, url):
    async with session.get(url) as response:
        return await response.text()

async def filter_spankbang_playlist(url):
    pattern = r"-(.*?)/playlist"
    modifed = re.sub(pattern, "/playlist", url)
    return modifed

async def spankbang_playlist_fetch(url, user_id):

    if user_id in temp.PLAYLIST_DOWNLOAD:
        return 0

    else:
        temp.PLAYLIST_DOWNLOAD[user_id] = []

    async with aiohttp.ClientSession() as session:
        try:
            response = await fetch_page(session, url)
            soup = BeautifulSoup
            (response, "html5lib")

            try:
                page_links = soup.find("div", attrs={"class": "pagination"}).findAll(
                    "a", href=True
                )
            except:
                page_links = [0]

            page_urls = [f"{url}/{i}" for i in range(1, len(page_links) + 1)]

            tasks = [fetch_page(session, page_url) for page_url in page_urls]
            pages = await asyncio.gather(*tasks)

            for page_html in pages:
                sp = BeautifulSoup(page_html, "html5lib")
                videos = sp.find(
                    "div",
                    attrs={"class": "video-list video-rotate video-list-with-ads"},
                ).findAll("a", attrs={"class": "thumb"})
                for link in videos:
                    video_link = "https://spankbang.party" + link["href"]
                    temp.PLAYLIST_DOWNLOAD[user_id].append(video_link)

        except Exception as e:
            print(
                "Error on line {}".format(sys.exc_info()[-1].tb_lineno),
                type(e).__name__,
                e,
            )
            return 0

    return 1

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + "ᴅ, ") if days else "")
        + ((str(hours) + "ʜ, ") if hours else "")
        + ((str(minutes) + "ᴍ, ") if minutes else "")
        + ((str(seconds) + "ꜱ, ") if seconds else "")
        + ((str(milliseconds) + "ᴍꜱ, ") if milliseconds else "")
    )
    return tmp[:-2]


async def fetch_shorturl(shorturl):
    async with aiohttp.ClientSession() as session:
        async with session.get(shorturl) as response:
            return await response.text()

def strip_ansi_codes(text: str) -> str:
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

# Async handler for progress updates
async def handle_progress(queue: Queue, ms):
    while True:
        progress = await asyncio.to_thread(queue.get)
        if progress is None:  # Stop signal
            break
        try:
            await ms.edit(progress)
        except Exception:
            pass

def progress_hook(d, queue: Queue):
    if d['status'] == 'downloading':
        percent = strip_ansi_codes(d.get('_percent_str', '0%').strip())
        speed = strip_ansi_codes(d.get('_speed_str', 'N/A'))
        eta = strip_ansi_codes(d.get('_eta_str', 'N/A'))
        text = f"**Downloading...**\n\n**Progress:** `{percent}`\n**Speed:** `{speed}`\n**ETA:** `{eta}`"
        queue.put(text)


async def start_clone_bot(userBot):
    await userBot.start()
    return userBot


def client(session):
    return Client("USERBOT", Config.API_ID, Config.API_HASH, session_string=session)

def str_to_b64(__str: str) -> str:
    str_bytes = __str.encode("ascii")
    bytes_b64 = standard_b64encode(str_bytes)
    b64 = bytes_b64.decode("ascii")
    return b64


def b64_to_str(b64: str) -> str:
    bytes_b64 = b64.encode("ascii")
    bytes_str = standard_b64decode(bytes_b64)
    __str = bytes_str.decode("ascii")
    return __str

async def send_log(b, u):
    if Config.LOG_CHANNEL is not None:
        curr = datetime.now(timezone("Asia/Kolkata"))
        date = curr.strftime("%d %B, %Y")
        time_str = curr.strftime("%I:%M:%S %p")
        await b.send_message(
            Config.LOG_CHANNEL,
            f"**--Nᴇᴡ Uꜱᴇʀ Sᴛᴀʀᴛᴇᴅ Tʜᴇ Bᴏᴛ--**\n\n"
            f"Uꜱᴇʀ: {u.mention}\nIᴅ: `{u.id}`\nUɴ: @{u.username}\n\n"
            f"Dᴀᴛᴇ: {date}\nTɪᴍᴇ: {time_str}\n\nBy: {b.mention}",
        )



def is_plan_expire(formatted_date):
    # Convert formatted_date string to datetime object
    expire_date = datetime.strptime(formatted_date, "%Y-%m-%d")

    # Get current date
    current_date = datetime.now()

    # Compare current date with expire_date
    if current_date > expire_date:
        return True
    else:
        return False

def is_token_expired(formatted_date):

    # Convert the string back to a datetime object
    formatted_next_day_datetime = datetime.strptime(formatted_date, "%Y-%m-%d %H:%M:%S")
    
    # Get the current date and time
    now =  datetime.now()  
    
    # Compare the current date and time with the stored datetime
    if now > formatted_next_day_datetime:
        return True
    else:
        return False

async def extract_number_and_remove(string):
    # Define a regular expression pattern to match the number at the end of the string
    pattern = r"(\d+)$"

    # Use re.search to find the match in the string
    match = re.search(pattern, string)

    # If a match is found, extract the number and remove it from the string
    if match:
        number = int(match.group())
        string_without_number = string[: match.start()].strip()
        return number, string_without_number
    else:
        return None, string


async def extract_percentage(string):
    # Define a regular expression pattern to match the percentage at the end of the string
    pattern = r"\b\d+(?:\.\d+)?%"

    # Use re.search to find the match in the string
    match = re.search(pattern, string)

    # If a match is found, extract the percentage
    if match:
        percentage = match.group()
        return percentage
    else:
        return None


async def fix_thumb(thumb):
    width = 0
    height = 0
    try:
        if thumb != None:
            # Open the image file
            with Image.open(thumb) as img:
                width = img.width
                height = img.height
                # Resize the image if its height is greater than 320 pixels
                if height > 320:
                    ratio = 320 / height
                    width = int(width * ratio)
                    height = 320
                    img = img.resize((width, height), Image.LANCZOS)
                    img.convert("RGB").save(thumb)
                else:
                    # Resize the image
                    resized_img = img.resize((width, height))
                    resized_img.convert("RGB").save(thumb)
    except Exception as e:
        print(e)
        thumb = None
    return width, height, thumb