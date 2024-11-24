import asyncio
from yt_dlp import YoutubeDL
from concurrent.futures import ThreadPoolExecutor
from utility.constant import QUALITIES


executor = ThreadPoolExecutor(max_workers=5)

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


async def get_xhamster_video_info(link: str) -> dict:
    result = {}
    ydl_opts = {}  # Options for yt_dlp

    # Define a blocking function to use with an executor
    def fetch_video_info():
        with YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(link, download=False)

    try:
        # Run the blocking function in ThreadPoolExecutor
        loop = asyncio.get_event_loop()
        info = await loop.run_in_executor(executor, fetch_video_info)

        # Process the extracted information
        result.update({"title": info.get("title")})
        result.update({"duration": seconds_to_readable_time(info.get("duration"))})
        result.update({"thumbnail": info.get("thumbnail")})
        result.update({"description": info.get("description")})

        # Extract download links based on resolution
        result.update({"videos": {}})
        for item in info["formats"]:
            if item["resolution"] in QUALITIES:
                result["videos"].update({item["resolution"]: item["url"]})
        return result

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}
