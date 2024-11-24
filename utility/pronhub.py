import asyncio
from concurrent.futures import ThreadPoolExecutor
import yt_dlp
from utility.constant import QUALITIES

# Create a ThreadPoolExecutor for blocking operations
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

async def get_pornhub_video_info(link: str) -> dict:
    result = {}
    ydl_opts = {}  # Options for yt_dlp

    # Define the blocking operation
    def fetch_video_info():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(link, download=False)

    try:
        # Run the blocking function in a thread pool
        loop = asyncio.get_event_loop()
        info = await loop.run_in_executor(executor, fetch_video_info)

        # Process video information
        result.update({"title": info.get("title")})
        result.update({"duration": seconds_to_readable_time(info.get("duration"))})
        result.update({"thumbnail": info.get("thumbnail")})
        result.update({"description": None})  # Set description as None if not provided

        # Extract download links
        result.update({"videos": {}})
        for item in info["formats"]:
            if item["format_id"] in QUALITIES:
                result["videos"].update({item["format_id"]: item["url"]})

        return result

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}
