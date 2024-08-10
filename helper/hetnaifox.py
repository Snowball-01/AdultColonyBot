import asyncio
import os
import random
import time
import logging
import aiohttp
import aiofiles
import img2pdf
from helper.utils import progress_for_pyrogram, download_thumbnail
from config import temp
from PIL import Image


# Configure logging settings
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def remove_invalid_characters(input_string):
    # Define a list of invalid characters
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']

    # Remove invalid characters from the input string
    cleaned_string = ''.join(
        char for char in input_string if char not in invalid_chars)

    return cleaned_string


async def remove_downloaded_images(user_id, image_urls):
    for url in image_urls:
        image_name = url.split('/')[-1]
        file_path = f"downloads/{user_id}/{image_name}"
        try:
            os.remove(file_path)
        except FileNotFoundError:
            pass


async def download_image(url, filename, retries=3, delay=5):
    for attempt in range(retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=60) as response:
                    async with aiofiles.open(filename, 'wb') as f:
                        await f.write(await response.read())

            return  # If download is successful, exit the loop
        except aiohttp.ClientError as e:
            logging.error(f"Error downloading image from {url}: {e}")
            if attempt < retries - 1:
                # Calculate exponential backoff delay
                backoff_delay = delay * 2 ** attempt
                logging.warning(
                    f"Retrying download {attempt + 1}/{retries} in {backoff_delay} seconds...")
                await asyncio.sleep(backoff_delay)
            else:
                logging.error(
                    f"Failed to download image from {url} after {retries} attempts.")


async def convert_images_to_pdf(image_urls, bot, message, source, title, process):
    try:
        clean_string = remove_invalid_characters(title)
        output = f"downloads/{message.from_user.id}/{clean_string}.pdf"

        # Create a list of tasks for downloading images

        for url in image_urls:
            await download_image(url, f"downloads/{message.from_user.id}/{url.split('/')[-1]}")

        # Define A4 page size in millimeters
        a4_size_mm = (210, 297)
        # Convert A4 size from millimeters to points (1 inch = 25.4 mm, 1 inch = 72 points)
        a4_size_points = tuple(mm * 72 / 25.4 for mm in a4_size_mm)

        # Specify the layout parameters including page size
        layout_fun = img2pdf.get_layout_fun(
            pagesize=(a4_size_points[0], a4_size_points[1])
        )
        # Convert images to PDF asynchronously

        async def convert_to_pdf():
            with open(output, "wb") as f:
                f.write(img2pdf.convert(
                    [f"downloads/{message.from_user.id}/{url.split('/')[-1]}" for url in image_urls], layout_fun=layout_fun))
            logging.info('PDF created.')

        await convert_to_pdf()

        # Remove downloaded images asynchronously
        await remove_downloaded_images(message.from_user.id, image_urls)

        # Generate thumbnail
        unique_id = random.randint(1000, 9999)
        thumbnail_filename = f"thumbnail_{unique_id}.jpg"
        await download_thumbnail(image_urls[0], thumbnail_filename)

        # Send PDF document
        caption = f"<b>ᴛɪᴛʟᴇ :- </b> `{title}`\n\n<b>sᴏᴜʀᴄᴇ :- </b> {source}\n\n<b>🍀 Developer </b> <a href=https://t.me/Snowball_official>ѕησωвαℓℓ ❄️</a>"
        await process.delete()
        ms = await message.reply_text("**⚠️Please Wait....**\n\n**Trying to Upload ☁️**")
        await bot.send_document(chat_id=message.from_user.id, document=output, thumb=thumbnail_filename, caption=caption, progress=progress_for_pyrogram, progress_args=("⚠️ Please wait...\n\n**Uploading started... ❄️**", ms, time.time()), reply_to_message_id=message.id)
        await ms.delete()

        # Clean up files using asyncio
        os.remove(output)
        os.remove(thumbnail_filename)
        temp.PENDING_DOWNLOADS.remove(message.from_user.id)

    except Exception as e:
        # Log any errors that occur
        logging.error('Error occurred:', exc_info=True)
