import json
import re
import httpx
from lxml import html
import ast
from utility.constant import QUALITIES


def convert_duration(duration):
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
    if match:
        hours = int(match.group(1)) if match.group(1) else 0
        minutes = int(match.group(2)) if match.group(2) else 0
        seconds = int(match.group(3)) if match.group(3) else 0
        if hours > 0:
            return f"{hours}:{minutes:02}:{seconds:02} hours"
        elif minutes > 0:
            return f"{minutes}:{seconds:02} minutes"
        else:
            return f"{seconds} seconds"
    return "Invalid duration format"


async def fetch_content(link: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(link, timeout=30)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.text


async def get_spankbang_video_info(link: str) -> dict:
    result = {}
    try:
        # Fetch page content asynchronously
        page_content = await fetch_content(link)
        tree = html.fromstring(page_content)

        # Content info logic 🍃
        content_data = tree.xpath("//script[@type='application/ld+json']/text()")
        if content_data:
            json_data = json.loads(content_data[0])
            result.update({
                "title": json_data.get("name"),
                "duration": convert_duration(json_data.get("duration")),
                "thumbnail": json_data.get("thumbnailUrl"),
                "description": json_data.get("description")
            })

        # Download link logic 🍃
        script = tree.xpath("//script[contains(text(), 'var stream_data =')]/text()")
        if script:
            match = re.search(r'var stream_data = (\{.*?\});', script[0])
            if match:
                stream_data = ast.literal_eval(match.group(1))
                result["videos"] = {
                    quality: url[0]
                    for quality, url in stream_data.items()
                    if quality in QUALITIES and url
                }
        return result

    except httpx.RequestError as e:
        print(f"Request error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return {}
