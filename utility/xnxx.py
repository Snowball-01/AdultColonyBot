import asyncio
from concurrent.futures import ThreadPoolExecutor
import yt_dlp
from utility.constant import QUALITIES


def seconds_to_readable_time(seconds):
    seconds = int(seconds)
    # Handle seconds
    if seconds < 60:
        return f"{seconds} seconds"

    # Calculate hours, minutes, and remaining seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    # Format output based on time components
    if hours > 0:
        return f"{hours}:{minutes:02}:{seconds:02} hours"
    elif minutes > 0:
        return f"{minutes}:{seconds:02} minutes"
    else:
        return f"{seconds} seconds"


# Create a ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=5)


async def get_xnxx_video_info(link: str) -> dict:
    result = {}

    def fetch_video_info():
        ydl_opts = {}  # Options for yt_dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(link, download=False)

    try:
        # Run the blocking function in the thread pool
        loop = asyncio.get_event_loop()
        info = await loop.run_in_executor(executor, fetch_video_info)

        # Content info logic 🍃
        result.update({"title": info.get("title")})
        result.update({"duration": seconds_to_readable_time(info.get("duration"))})
        result.update({"thumbnail": info.get("thumbnail")})
        result.update({"description": None})

        # Download link logic 🍃
        result.update({"videos": {}})
        for item in info["formats"]:
            if item["format_id"].startswith("hls") and item["format_id"].split('-')[1] in QUALITIES:
                result["videos"].update({item["format_id"].split('-')[1]: item["url"]})

        return result

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}
