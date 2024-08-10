import math
import os
import re
import sys
import time
import asyncio
import logging
import aiofiles
import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
import requests
from pyrogram import Client
import youtube_dl
from config import Config, Txt, temp
from PIL import Image
from moviepy.editor import VideoFileClip
from base64 import standard_b64encode, standard_b64decode
import cloudscraper
import subprocess

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def start_clone_bot(userBot):
    await userBot.start()
    return userBot


def client(session):
    return Client("USERBOT", Config.API_ID, Config.API_HASH, session_string=session)


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


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)


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


# async def run_async(func, *args, **kwargs):
#     loop = asyncio.get_running_loop()
#     return await loop.run_in_executor(None, lambda: func(*args, **kwargs))


# def edit_msg(client, message, to_edit):
#     try:
#         client.loop.create_task(message.edit(to_edit))
#     except FloodWait as e:
#         client.loop.create_task(asyncio.sleep(e.value))
#     except MessageNotModified:
#         pass
#     except TypeError:
#         pass


# def download_progress_hook(d, message, client):
#     if d['status'] == 'downloading':
#         current = d.get("_downloaded_bytes_str") or humanbytes(
#             int(d.get("downloaded_bytes", 1)))
#         total = d.get("_total_bytes_str") or d.get("_total_bytes_estimate_str")
#         file_name = d.get("filename").split('/')[-1]
#         eta = d.get('_eta_str', "N/A")
#         percent = d.get("_percent_str", "N/A")
#         speed = d.get("_speed_str", "N/A")
#         to_edit = f"📥 <b>Downloading!</b>\n\n<b>Name :</b> <code>{file_name}</code>\n<b>Size :</b> <code>{total}</code>\n<b>Speed :</b> <code>{speed}</code>\n<b>ETA :</b> <code>{eta}</code>\n\n<b>Percentage: </b> <code>{current}</code> from <code>{total} (__{percent}__)</code>"
#         threading.Thread(target=edit_msg, args=(
#             client, message, to_edit)).start()


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


async def decode_jav_links(p, a, c, k):
    def base_convert(number, base):
        """Convert a number to a string in a given base (up to base 36)."""
        if number < 0:
            sign = -1
        elif number == 0:
            return "0"
        else:
            sign = 1

        number *= sign
        digits = []

        while number:
            digits.append(int(number % base))
            number //= base

        if sign < 0:
            digits.append("-")

        digits.reverse()

        return "".join(
            str(digit) if digit < 10 else chr(digit + 87) for digit in digits
        )

    while c:
        c -= 1
        base_c_str = base_convert(c, a)
        if k[c]:
            p = re.sub(
                r"\b" + re.escape(base_c_str) + r"\b", k[c], p, flags=re.IGNORECASE
            )
    return p


async def file_data(string):
    extract_data = lambda trailed: (
        trailed[: trailed.find("}}}}'") + 5],
        list(trailed[trailed.find("}}}}'") + 6 :].split(",")),
    )
    file_data = extract_data(string[114:-3])
    data = await decode_jav_links(
        file_data[0], int(file_data[1][0]), int(file_data[1][1]), eval(file_data[1][2])
    )
    return data


async def extract_m3u8_url(raw_url):

    if "javhd.today" in raw_url:
        r = requests.get(raw_url)
        streamwish = BeautifulSoup(r.text, "html5lib")
        allbtn = streamwish.findAll("button1", attrs={"class": "button_choice_server"})

        allinks = [link["onclick"] for link in allbtn]
        # Regular expression to match URLs
        pattern = r"playEmbed\('([^']*)'\)"

        # Extracting URLs
        urls = [re.search(pattern, link).group(1) for link in allinks]
        link = [link for link in urls if "kissmovies" in link]
        if not link:
            return None

        scraper = cloudscraper.create_scraper()
        info = scraper.get(link[0])
        soup = BeautifulSoup(info.text, "html5lib")

        # Find the JavaScript variable containing the setup parameters
        script = soup.findAll("script", attrs={"type": "text/javascript"})[3]
        fileData = await file_data(script.string)
        match = re.search(r'file:"([^"]+)"', str(fileData))
        if match:
            file_url = match.group(1)
            return file_url
        else:
            return None

    elif "javtsunami.com" in raw_url:
        scrap = cloudscraper.create_scraper()
        r = scrap.get(raw_url)
        response = BeautifulSoup(r.text, "html5lib")
        script = [link.get("src") for link in response.find_all("iframe")]
        script = [link for link in script if "hicherri.com" in link]
        if not script:
            return None
        
        link = scrap.get(script[0])
        getLink = BeautifulSoup(link.text, "html5lib")
        fileData = await file_data(
            getLink.findAll("script", attrs={"type": "text/javascript"})[3].string
        )

        match = re.search(r'file:"([^"]+)"', str(fileData))
        if match:
            file_url = match.group(1)
            return file_url
        else:
            return None

    elif "javgiga.com" in raw_url:
        scrap = cloudscraper.create_scraper()
        r = scrap.get(raw_url)
        response = BeautifulSoup(r.text, "html5lib")
        script = [link.get("src") for link in response.find_all("iframe")]
        script = [link for link in script if "javtiktok.site" in link]
        if not script:
            return None
        
        link = scrap.get(script[0])
        getLink = BeautifulSoup(link.text, "html5lib")
        fileData = await file_data(
            getLink.findAll("script", attrs={"type": "text/javascript"})[3].string
        )

        match = re.search(r'file:"([^"]+)"', str(fileData))
        if match:
            file_url = match.group(1)
            return file_url
        else:
            return None

    else:
        return None


async def download_m3u8_with_ffmpeg(message, url, output_file):

    await message.edit("**ᴠᴇʀɪғʏɪɴɢ ᴛʜᴇ sᴏᴜʀᴄᴇ** ⌛")
    # Use ffmpeg to download the M3U8 stream and save it to a file
    cmd = f"ffmpeg -threads 4 -i {url} -c copy {output_file}"
    process = await asyncio.create_subprocess_exec(
        *cmd.split(), stderr=asyncio.subprocess.PIPE
    )

    total_duration = None  # Initialize total duration to None
    bar_length = 20  # Define the length of the progress bar

    while True:
        line = await process.stderr.readline()
        if not line:
            break
        line = line.decode().strip()
        if "Duration" in line:
            # Extract total duration from the first line containing "Duration"
            duration_match = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", line)
            if duration_match:
                hours, minutes, seconds = map(float, duration_match.groups())
                total_duration = hours * 3600 + minutes * 60 + seconds

        if "time=" in line and "bitrate=" in line and total_duration:
            time_index = line.index("time=")
            bitrate_index = line.index("bitrate=")
            time_str = line[time_index + 5 : bitrate_index - 2]
            time_components = time_str.split(":")
            if len(time_components) == 3:
                hours = int(time_components[0])
                minutes = int(time_components[1])
                seconds = float(time_components[2])
                total_seconds = hours * 3600 + minutes * 60 + seconds
                progress = (total_seconds / total_duration) * 100
                # Calculate progress bar
                completed_length = int(progress / (100 / bar_length))
                remaining_length = bar_length - completed_length
                progress_bar = (
                    "[" + "⬢" * completed_length + "⬡" * remaining_length + "]"
                )

                try:
                    await message.edit(
                        f"📥 **ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ sᴛᴀʀᴛᴇᴅ...**\n\n`{progress:.2f}%` **{progress_bar}**\n\n>⚠️ ᴡʜʏ sʟᴏᴡ :- Fɪʀsᴛʟʏ, ᴛʜᴇ ᴠɪᴅᴇᴏs ᴏɴ ᴛʜᴇ sɪᴛᴇs ᴇᴍᴘʟᴏʏ ʀᴏʙᴜsᴛ DMC ᴄᴏɴᴛᴇɴᴛ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ ᴍᴇᴄʜᴀɴɪsᴍs, ʀᴇɴᴅᴇʀɪɴɢ ᴛʜᴇ ᴇxᴛʀᴀᴄᴛɪᴏɴ ᴏғ ᴠɪᴅᴇᴏ ᴅᴀᴛᴀ ᴀʀᴅᴜᴏᴜs. Sᴇᴄᴏɴᴅʟʏ, ᴀʟʟ ᴛʜᴇ ᴠɪᴅᴇᴏs ʜᴏsᴛᴇᴅ ᴏɴ ᴛʜɪs ᴘʟᴀᴛғᴏʀᴍ ʙᴏᴀsᴛ ғɪʟᴇ sɪᴢᴇs ᴍᴇᴀsᴜʀᴇᴅ ɪɴ ɢɪɢᴀʙʏᴛᴇs, ᴀᴛᴛʀɪʙᴜᴛᴀʙʟᴇ ᴛᴏ ᴛʜᴇɪʀ ᴇxᴛᴇɴᴅᴇᴅ ᴅᴜʀᴀᴛɪᴏɴ ʀᴀɴɢɪɴɢ ғʀᴏᴍ 2 ᴛᴏ 4 ʜᴏᴜʀs ᴘᴇʀ ᴍᴏᴠɪᴇ."
                    )
                except:
                    pass

    # Wait for the process to finish
    await process.wait()
    return


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


async def filter_spankbang_playlist(url):
    pattern = r"-(.*?)/playlist"
    modifed = re.sub(pattern, "/playlist", url)
    return modifed


async def get_thumbnail(video_url):

    if "spankbang.party" in video_url:
        return await get_spank_bang_thumb(video_url=video_url)

    elif "xhamster.com" in video_url:
        return await get_xhamster_thumb(video_url=video_url)

    elif "japanhdv.com" in video_url:
        return await get_japanhdv_thumb(video_url=video_url)

    elif "japteenx.com" in video_url:
        return await get_japteenx_thumb(video_url=video_url)

    elif "kissjav.com" in video_url:
        return await get_kissjav_thumb(video_url=video_url)

    elif "eporner.com" in video_url:
        return await get_eporner_thumb(video_url=video_url)

    elif "javhd.today" in video_url:
        return await get_javhdtoday_thumb(video_url=video_url)

    elif "javhd.icu" in video_url:
        return await get_javhdicu_thumb(video_url=video_url)

    ydl_opts = {
        "format": "best",
        "quiet": True,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(video_url, download=False)
            return info_dict.get("thumbnail")
        except Exception as e:
            return None


async def get_spank_bang_thumb(video_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(video_url) as response:
            if response.status != 200:
                return None
            html_content = await response.text()

    thumb = BeautifulSoup(html_content, "html5lib")

    return thumb.find("img", attrs={"class": "lazyload player_thumb"})["data-src"]


async def get_xhamster_thumb(video_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(video_url) as response:
            if response.status != 200:
                return None
            html_content = await response.text()

    thumb = BeautifulSoup(html_content, "html5lib")
    return thumb.find("div", attrs={"class": "xp-preload-image"})["style"].split("'")[1]


async def get_japanhdv_thumb(video_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(video_url) as response:
            if response.status != 200:
                return None
            html_content = await response.text()

    thumb = BeautifulSoup(html_content, "html5lib")
    url = thumb.find("video", attrs={"preload": "none"})["poster"][2:]
    return f"https://{url}"


async def get_japteenx_thumb(video_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(video_url) as response:
            if response.status != 200:
                return None
            html_content = await response.text()

    thumb = BeautifulSoup(html_content, "html5lib")
    return thumb.find("video", attrs={"preload": "auto"})["poster"]


async def get_kissjav_thumb(video_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(video_url) as response:
            if response.status != 200:
                return None
            html_content = await response.text()

    thumb = BeautifulSoup(html_content, "html5lib")
    thumburl = thumb.find("video", attrs={"preload": "none"})["poster"]
    thumb = f"https://kissjav.com{thumburl}"
    return thumb


async def get_eporner_thumb(video_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(video_url) as response:
            if response.status != 200:
                return None
            html_content = await response.text()

    thumb = BeautifulSoup(html_content, "html5lib")
    return thumb.find("video", attrs={"id": "EPvideo"})["poster"]


async def get_javhdtoday_thumb(video_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(video_url) as response:
            if response.status != 200:
                return None
            html_content = await response.text()

    thumb = BeautifulSoup(html_content, "html5lib")
    return thumb.find("div", attrs={"class": "col-xs-12 col-sm-6 col-md-4"}).find(
        "img"
    )["src"]


async def get_javhdicu_thumb(video_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(video_url) as response:
            if response.status != 200:
                return None
            html_content = await response.text()

    thumb = BeautifulSoup(html_content, "html5lib")
    return thumb.findAll("meta", attrs={"property": "og:image:secure_url"})[0][
        "content"
    ]


async def download_thumbnail(thumbnail_url, thumbnail_path):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail_url) as response:
            if response.status == 200:
                async with aiofiles.open(thumbnail_path, "wb") as f:
                    await f.write(await response.read())


async def get_video_durations(file_path):
    try:
        clip = VideoFileClip(file_path)
        duration = clip.duration
        clip.close()
        return duration
    except Exception as e:
        return None


async def format_duration(duration):
    hours = int(duration // 3600)
    minutes = int((duration % 3600) // 60)
    seconds = int(duration % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


async def fetch_page(session, url):
    async with session.get(url) as response:
        return await response.text()


async def spankbang_playlist_fetch(url, user_id):

    if user_id in temp.PLAYLIST_DOWNLOAD:
        return 0

    else:
        temp.PLAYLIST_DOWNLOAD[user_id] = []

    async with aiohttp.ClientSession() as session:
        try:
            response = await fetch_page(session, url)
            soup = BeautifulSoup(response, "html5lib")

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


def get_file_size(file_path):
    return os.path.getsize(file_path)


async def split_file_by_size(input_file, max_part_size_mb, file_name, user_id):
    max_part_size = max_part_size_mb * 1024 * 1024  # Convert MB to bytes
    total_size = get_file_size(input_file)
    part_num = 1
    start_time = 0

    # Calculate the duration of the input file
    result = subprocess.run(
        ["ffmpeg", "-i", input_file], stderr=subprocess.PIPE, stdout=subprocess.PIPE
    )
    duration_line = [
        x for x in result.stderr.decode("utf-8").split("\n") if "Duration" in x
    ][0]
    duration_str = duration_line.split(" ")[3].strip().strip(",")
    h, m, s = duration_str.split(":")
    total_duration = int(h) * 3600 + int(m) * 60 + float(s)

    # Calculate the size ratio
    size_ratio = total_size / total_duration

    while total_size > 0:
        part_size = min(max_part_size, total_size)
        part_duration = part_size / size_ratio
        output_file = f"downloads/{user_id}/{file_name} - Part {part_num}.mp4"

        command = [
            "ffmpeg",
            "-y",  # Overwrite output files without asking
            "-ss",
            str(start_time),
            "-t",
            str(part_duration),
            "-i",
            input_file,
            "-c",
            "copy",
            output_file,
        ]

        subprocess.run(command)

        start_time += part_duration
        total_size -= part_size
        part_num += 1
