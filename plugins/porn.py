import random
import re
import aiohttp
from pornhub_api import PornhubApi
from pornhub_api.backends.aiohttp import AioHttpBackend
from pyrogram.types import (InlineKeyboardButton,
                            InlineKeyboardMarkup, InlineQuery,
                            InlineQueryResultArticle, InputTextMessageContent)
from pyrogram import Client
from config import Config
from helper.utils import extract_number_and_remove, extract_percentage


@Client.on_inline_query()
async def search(client, InlineQuery: InlineQuery):
    query = InlineQuery.query

    backend = AioHttpBackend()
    api = PornhubApi(backend=backend)
    results = []

    if query.strip().lower().startswith("@xnxx"):
        userquery = re.sub("@xnxx", "", query.strip().lower()).strip()

        if userquery.isnumeric():
            page = userquery
            userquery = 'bbc'
        else:
            number, string_without_number = await extract_number_and_remove(
                userquery)
            if number:
                page = number
                userquery = string_without_number
            else:
                page = 1

            if userquery == "":
                userquery = 'bbc'

        async with aiohttp.ClientSession() as session:
            async with session.get(f'{Config.API}/xnxx/search?key={userquery}&page={page}') as resp:
                response = await resp.json()
                data = response['data']

                for video in data:
                    rating = await extract_percentage(video['rating'])
                    views = re.sub(rating, "", video['rating']).strip()
                    results.append(InlineQueryResultArticle(
                        title=video['title'],
                        input_message_content=InputTextMessageContent(
                            message_text=video['link']
                        ),
                        description=f"Dᴜʀᴀᴛɪᴏɴ : {video['duration']}\nVɪᴇᴡs : {views}\nRᴀᴛɪɴɢ : {rating}",
                        thumb_url=video['image'],
                        reply_markup=InlineKeyboardMarkup([[
                            InlineKeyboardButton(
                                "Wᴀᴛᴄʜ Oɴʟɪɴᴇ", url=video['link']),
                            InlineKeyboardButton(
                                "Sᴇᴀʀᴄʜ Mᴏʀᴇ", switch_inline_query_current_chat=f"{query}")
                        ]])
                    ))
        await InlineQuery.answer(results, switch_pm_text=f"Search Results", switch_pm_parameter="start")
        return

    elif query.strip().lower().startswith("@xvideos"):
        userquery = re.sub("@xvideos", "", query.strip().lower()).strip()

        if userquery.isnumeric():
            page = userquery
            userquery = 'hentai'
        else:
            number, string_without_number = await extract_number_and_remove(
                userquery)
            if number:
                page = number
                userquery = string_without_number
            else:
                page = 1

            if userquery == "":
                userquery = 'hentai'

        async with aiohttp.ClientSession() as session:
            async with session.get(f'{Config.API}/xvideos/search?key={userquery}&page={page}') as resp:
                response = await resp.json()
                data = response['data']
                for video in data:
                    results.append(InlineQueryResultArticle(
                        title=video['title'],
                        input_message_content=InputTextMessageContent(
                            message_text=video['link']
                        ),
                        description=f"Dᴜʀᴀᴛɪᴏɴ : {video['duration']}",
                        thumb_url=video['image'],
                        reply_markup=InlineKeyboardMarkup([[
                            InlineKeyboardButton(
                                "Wᴀᴛᴄʜ Oɴʟɪɴᴇ", url=video['link']),
                            InlineKeyboardButton(
                                "Sᴇᴀʀᴄʜ Mᴏʀᴇ", switch_inline_query_current_chat=f"{query}")
                        ]])
                    ))
        await InlineQuery.answer(results, switch_pm_text=f"Search Results", switch_pm_parameter="start")
        return

    elif query.strip().lower().startswith("@xhamster"):
        userquery = re.sub("@xhamster", "", query.strip().lower()).strip()

        if userquery.isnumeric():
            page = userquery
            userquery = 'arab'
        else:
            number, string_without_number = await extract_number_and_remove(
                userquery)
            if number:
                page = number
                userquery = string_without_number
            else:
                page = 1

            if userquery == "":
                userquery = 'arab'

        async with aiohttp.ClientSession() as session:
            async with session.get(f'{Config.API}/xhamster/search?key={userquery}&page={page}') as resp:
                response = await resp.json()
                data = response['data']
                for video in data:
                    results.append(InlineQueryResultArticle(
                        title=video['title'],
                        input_message_content=InputTextMessageContent(
                            message_text=video['link']
                        ),
                        description=f"Dᴜʀᴀᴛɪᴏɴ : {video['duration']}\nVɪᴇᴡs : {video['views']}",
                        thumb_url=video['image'],
                        reply_markup=InlineKeyboardMarkup([[
                            InlineKeyboardButton(
                                "Wᴀᴛᴄʜ Oɴʟɪɴᴇ", url=video['link']),
                            InlineKeyboardButton(
                                "Sᴇᴀʀᴄʜ Mᴏʀᴇ", switch_inline_query_current_chat=f"{query}")
                        ]])
                    ))
        await InlineQuery.answer(results, switch_pm_text=f"Search Results", switch_pm_parameter="start")
        return

    elif query.strip().lower().startswith("@spankbang"):
        userquery = re.sub("@spankbang", "", query.strip().lower()).strip()

        if userquery.isnumeric():
            page = userquery
            userquery = 'japanese'
        else:
            number, string_without_number = await extract_number_and_remove(
                userquery)
            if number:
                page = number
                userquery = string_without_number
            else:
                page = 1

            if userquery == "":
                userquery = 'japanese'

        async with aiohttp.ClientSession() as session:
            async with session.get(f'{Config.API}/spankbang/search?key={userquery}&page={page}') as resp:
                response = await resp.json()
                data = response['data']

                for video in data[0:50]:
                    if video['link'].endswith('partyundefined'):
                        continue

                    results.append(InlineQueryResultArticle(
                        title=video['title'],
                        input_message_content=InputTextMessageContent(
                            message_text=video['link']
                        ),
                        description=f"Dᴜʀᴀᴛɪᴏɴ : {video['duration']}\nVɪᴇᴡs : {video['views']}\nRᴀᴛɪɴɢ : {video['rating']}",
                        thumb_url=video['image'],
                        reply_markup=InlineKeyboardMarkup([[
                            InlineKeyboardButton(
                                "Wᴀᴛᴄʜ Oɴʟɪɴᴇ", url=video['link']),
                            InlineKeyboardButton(
                                "Sᴇᴀʀᴄʜ Mᴏʀᴇ", switch_inline_query_current_chat=f"{query}")
                        ]])
                    ))
        await InlineQuery.answer(results, switch_pm_text=f"Search Results", switch_pm_parameter="start")
        return

    elif query.strip().lower().startswith("@japteenx"):
        userquery = re.sub("@japteenx", "", query.strip().lower()).strip()

        if userquery.isnumeric():
            page = userquery
            userquery = 'japanese'
        else:
            number, string_without_number = await extract_number_and_remove(
                userquery)
            if number:
                page = number
                userquery = string_without_number
            else:
                page = 1

            if userquery == "":
                userquery = 'japanese'

        async with aiohttp.ClientSession() as session:
            async with session.get(f'{Config.API}/japteenx/search?key={userquery}&page={page}') as resp:
                response = await resp.json()
                data = response['data']

                for video in data:
                    results.append(InlineQueryResultArticle(
                        title=video['title'],
                        input_message_content=InputTextMessageContent(
                            message_text=video['link']
                        ),
                        description=f"Dᴜʀᴀᴛɪᴏɴ : {video['duration']}\nVɪᴇᴡs : {video['views']}\nRᴀᴛɪɴɢ : {video['rating']}",
                        thumb_url=video['image'],
                        reply_markup=InlineKeyboardMarkup([[
                            InlineKeyboardButton(
                                "Wᴀᴛᴄʜ Oɴʟɪɴᴇ", url=video['link']),
                            InlineKeyboardButton(
                                "Sᴇᴀʀᴄʜ Mᴏʀᴇ", switch_inline_query_current_chat=f"{query}")
                        ]])
                    ))
        await InlineQuery.answer(results, switch_pm_text=f"Search Results", switch_pm_parameter="start")
        return

    elif query.strip().lower().startswith("@japanhdv"):
        userquery = re.sub("@japanhdv", "", query.strip().lower()).strip()

        if userquery.isnumeric():
            page = userquery
            userquery = 'japanese'
        else:
            number, string_without_number = await extract_number_and_remove(
                userquery)
            if number:
                page = number
                userquery = string_without_number
            else:
                page = 1

            if userquery == "":
                userquery = 'japanese'

        async with aiohttp.ClientSession() as session:
            async with session.get(f'{Config.API}/japanhdv/search?key={userquery}&page={page}') as resp:
                response = await resp.json()
                data = response['data']

                for video in data:
                    if video['link'].endswith('undefined'):
                        continue
                    results.append(InlineQueryResultArticle(
                        title=video['title'],
                        input_message_content=InputTextMessageContent(
                            message_text=video['link']
                        ),
                        description=f"Dᴜʀᴀᴛɪᴏɴ : {video['duration']}\nVɪᴇᴡs : {video['views']}\nRᴀᴛɪɴɢ : {video['rating']}",
                        thumb_url=video['image'],
                        reply_markup=InlineKeyboardMarkup([[
                            InlineKeyboardButton(
                                "Wᴀᴛᴄʜ Oɴʟɪɴᴇ", url=video['link']),
                            InlineKeyboardButton(
                                "Sᴇᴀʀᴄʜ Mᴏʀᴇ", switch_inline_query_current_chat=f"{query}")
                        ]])
                    ))
        await InlineQuery.answer(results, switch_pm_text=f"Search Results", switch_pm_parameter="start")
        return
    elif query.strip().lower().startswith("@kissjav"):
        userquery = re.sub("@kissjav", "", query.strip().lower()).strip()

        if userquery.isnumeric():
            page = userquery
            userquery = 'korean'
        else:
            number, string_without_number = await extract_number_and_remove(
                userquery)
            if number:
                page = number
                userquery = string_without_number
            else:
                page = 1

            if userquery == "":
                userquery = 'korean'

        async with aiohttp.ClientSession() as session:
            async with session.get(f'{Config.API}/kissjav/search?key={userquery}&page={page}') as resp:
                response = await resp.json()
                data = response['data']

                for video in data:
                    if video['link'].endswith('comundefined'):
                        continue
                    results.append(InlineQueryResultArticle(
                        title=video['title'],
                        input_message_content=InputTextMessageContent(
                            message_text=video['link']
                        ),
                        description=f"Dᴜʀᴀᴛɪᴏɴ : {video['duration']}\nVɪᴇᴡs : {video['views']}\nRᴀᴛɪɴɢ : {video['rating']}",
                        thumb_url=video['image'],
                        reply_markup=InlineKeyboardMarkup([[
                            InlineKeyboardButton(
                                "Wᴀᴛᴄʜ Oɴʟɪɴᴇ", url=video['link']),
                            InlineKeyboardButton(
                                "Sᴇᴀʀᴄʜ Mᴏʀᴇ", switch_inline_query_current_chat=f"{query}")
                        ]])
                    ))
        await InlineQuery.answer(results, switch_pm_text=f"Search Results", switch_pm_parameter="start")
        return

    elif query.strip().lower().startswith("@japteenx"):
        userquery = re.sub("@japteenx", "", query.strip().lower()).strip()

        if userquery.isnumeric():
            page = userquery
            userquery = 'japanese'
        else:
            number, string_without_number = await extract_number_and_remove(
                userquery)
            if number:
                page = number
                userquery = string_without_number
            else:
                page = 1

            if userquery == "":
                userquery = 'japanese'

        async with aiohttp.ClientSession() as session:
            async with session.get(f'{Config.API}/japteenx/search?key={userquery}&page={page}') as resp:
                response = await resp.json()
                data = response['data']

                for video in data:
                    results.append(InlineQueryResultArticle(
                        title=video['title'],
                        input_message_content=InputTextMessageContent(
                            message_text=video['link']
                        ),
                        description=f"Dᴜʀᴀᴛɪᴏɴ : {video['duration']}\nVɪᴇᴡs : {video['views']}\nRᴀᴛɪɴɢ : {video['rating']}",
                        thumb_url=video['image'],
                        reply_markup=InlineKeyboardMarkup([[
                            InlineKeyboardButton(
                                "Wᴀᴛᴄʜ Oɴʟɪɴᴇ", url=video['link']),
                            InlineKeyboardButton(
                                "Sᴇᴀʀᴄʜ Mᴏʀᴇ", switch_inline_query_current_chat=f"{query}")
                        ]])
                    ))
        await InlineQuery.answer(results, switch_pm_text=f"Search Results", switch_pm_parameter="start")
        return

    elif query.strip().lower().startswith("@eporner"):
        userquery = re.sub("@eporner", "", query.strip().lower()).strip()

        if userquery.isnumeric():
            page = userquery
            userquery = 'chinese'
        else:
            number, string_without_number = await extract_number_and_remove(
                userquery)
            if number:
                page = number
                userquery = string_without_number
            else:
                page = 1

            if userquery == "":
                userquery = 'chinese'

        async with aiohttp.ClientSession() as session:
            async with session.get(f'{Config.API}/eporner/search?key={userquery}&page={page}') as resp:
                response = await resp.json()
                data = response['data']

                for video in data:
                    results.append(InlineQueryResultArticle(
                        title=video['title'],
                        input_message_content=InputTextMessageContent(
                            message_text=video['link']
                        ),
                        description=f"Dᴜʀᴀᴛɪᴏɴ : {video['duration']}\nVɪᴇᴡs : {video['views']}\nRᴀᴛɪɴɢ : {video['rating']}",
                        thumb_url=video['image'],
                        reply_markup=InlineKeyboardMarkup([[
                            InlineKeyboardButton(
                                "Wᴀᴛᴄʜ Oɴʟɪɴᴇ", url=video['link']),
                            InlineKeyboardButton(
                                "Sᴇᴀʀᴄʜ Mᴏʀᴇ", switch_inline_query_current_chat=f"{query}")
                        ]])
                    ))
        await InlineQuery.answer(results, switch_pm_text=f"Search Results", switch_pm_parameter="start")
        return

    elif query.strip().lower().startswith("@hentaifox"):
        userquery = re.sub("@hentaifox", "", query.strip().lower()).strip()

        if userquery.isnumeric():
            page = userquery
            userquery = 'milf'
        else:
            number, string_without_number = await extract_number_and_remove(
                userquery)
            if number:
                page = number
                userquery = string_without_number
            else:
                page = 1

            if userquery == "":
                userquery = 'milf'

        async with aiohttp.ClientSession() as session:
            async with session.get(f'{Config.API}/hentaifox/search?key={userquery}&page={page}&sort=popular') as resp:
                response = await resp.json()
                data = response['data']

                for manga in data:
                    results.append(InlineQueryResultArticle(
                        title=manga['title'],
                        input_message_content=InputTextMessageContent(
                            message_text=manga['link']
                        ),
                        description=f"Iᴅ : {manga['id']}\nCᴀᴛᴇɢᴏʀʏ : {manga['category']}\nLᴀɴɢᴜᴀɢᴇ : {manga['language']}",
                        thumb_url=manga['image'],
                        reply_markup=InlineKeyboardMarkup([[
                            InlineKeyboardButton(
                                "Vɪᴇᴡ Oɴʟɪɴᴇ", url=manga['link']),
                            InlineKeyboardButton(
                                "Sᴇᴀʀᴄʜ Mᴏʀᴇ", switch_inline_query_current_chat=f"{query}")
                        ]])
                    ))
        await InlineQuery.answer(results, switch_pm_text=f"Search Results", switch_pm_parameter="start")
        return

    elif query.strip().lower().startswith("@javhdtoday"):
        userquery = re.sub("@javhdtoday", "", query.strip().lower()).strip()

        if userquery.isnumeric():
            page = userquery
            userquery = 'beautiful'
        else:
            number, string_without_number = await extract_number_and_remove(
                userquery)
            if number:
                page = number
                userquery = string_without_number
            else:
                page = random.randint(1, 10)

            if userquery == "":
                userquery = 'beautiful'

        async with aiohttp.ClientSession() as session:
            async with session.get(f'{Config.API}/javhdtoday/search?key={userquery}&page={page}') as resp:
                response = await resp.json()
                data = response['data']

                for video in data:
                    results.append(InlineQueryResultArticle(
                        title=video['title'],
                        input_message_content=InputTextMessageContent(
                            message_text=video['link']
                        ),
                        description=f"Dᴜʀᴀᴛɪᴏɴ : {video['duration'].strip()}\nUᴘʟᴏᴀᴅᴇᴅ ᴏɴ: {video['uploaded_on']}\nRᴀᴛɪɴɢ : {video['rating']}",
                        thumb_url=video['image'],
                        reply_markup=InlineKeyboardMarkup([[
                            InlineKeyboardButton(
                                "Wᴀᴛᴄʜ Oɴʟɪɴᴇ", url=video['link']),
                            InlineKeyboardButton(
                                "Sᴇᴀʀᴄʜ Mᴏʀᴇ", switch_inline_query_current_chat=f"{query}")
                        ]])
                    ))
        await InlineQuery.answer(results, switch_pm_text=f"Search Results", switch_pm_parameter="start")
        return

    elif query.strip().lower().startswith("@javtsunami"):
        userquery = re.sub("@javtsunami", "", query.strip().lower()).strip()

        if userquery.isnumeric():
            page = userquery
            userquery = 'new'
        else:
            number, string_without_number = await extract_number_and_remove(
                userquery)
            if number:
                page = number
                userquery = string_without_number
            else:
                page = random.randint(1, 10)

            if userquery == "":
                userquery = 'new'

        async with aiohttp.ClientSession() as session:
            async with session.get(f'{Config.API}/javtsunami/search?key={userquery}&page={page}') as resp:
                response = await resp.json()
                data = response['data']

                for video in data:
                    results.append(InlineQueryResultArticle(
                        title=video['title'],
                        input_message_content=InputTextMessageContent(
                            message_text=video['link']
                            
                        ),
                        description=f"Vɪᴇᴡs : {video['views']}\nDᴜʀᴀᴛɪᴏɴ: {video['duration']}",
                        thumb_url=video['image'],
                        reply_markup=InlineKeyboardMarkup([[
                            InlineKeyboardButton(
                                "Wᴀᴛᴄʜ Oɴʟɪɴᴇ", url=video['link']),
                            InlineKeyboardButton(
                                "Sᴇᴀʀᴄʜ Mᴏʀᴇ", switch_inline_query_current_chat=f"{query}")
                        ]])
                    ))
        await InlineQuery.answer(results, switch_pm_text=f"Search Results", switch_pm_parameter="start")
        return

    elif query.strip().lower().startswith("@javgiga"):
        userquery = re.sub("@javgiga", "", query.strip().lower()).strip()

        if userquery.isnumeric():
            page = userquery
            userquery = 'new'
        else:
            number, string_without_number = await extract_number_and_remove(
                userquery)
            if number:
                page = number
                userquery = string_without_number
            else:
                page = random.randint(1, 10)

            if userquery == "":
                userquery = 'new'

        async with aiohttp.ClientSession() as session:
            async with session.get(f'{Config.API}/javgiga/search?key={userquery}&page={page}') as resp:
                response = await resp.json()
                data = response['data']

                for video in data:
                    results.append(InlineQueryResultArticle(
                        title=video['title'],
                        input_message_content=InputTextMessageContent(
                            message_text=video['link']
                            
                        ),
                        thumb_url=video['image'],
                        reply_markup=InlineKeyboardMarkup([[
                            InlineKeyboardButton(
                                "Wᴀᴛᴄʜ Oɴʟɪɴᴇ", url=video['link']),
                            InlineKeyboardButton(
                                "Sᴇᴀʀᴄʜ Mᴏʀᴇ", switch_inline_query_current_chat=f"{query}")
                        ]])
                    ))
        await InlineQuery.answer(results, switch_pm_text=f"Search Results", switch_pm_parameter="start")
        return

    try:
        src = await api.search.search(query)
    except ValueError as e:
        results.append(InlineQueryResultArticle(
            title="No Such Videos Found!",
            description="Sorry! No Such Videos Were Found. Please Try Again",
            input_message_content=InputTextMessageContent(
                message_text="No Such Videos Found!"
            )
        ))
        await InlineQuery.answer(results, switch_pm_text="Search Results", switch_pm_parameter="start")
        return

    videos = src.videos
    await backend.close()

    for vid in videos:
        try:
            pornstars = ", ".join(v for v in vid.pornstars)
            categories = ", ".join(v for v in vid.categories)
            tags = ", #".join(v for v in vid.tags)
        except:
            pornstars = "N/A"
            categories = "N/A"
            tags = "N/A"
        msg = (f"**TITLE** : `{vid.title}`\n"
               f"**DURATION** : `{vid.duration}`\n"
               f"VIEWS : `{vid.views}`\n\n"
               f"**{pornstars}**\n"
               f"Categories : {categories}\n\n"
               f"{tags}"
               f"Link : {vid.url}")

        results.append(InlineQueryResultArticle(
            title=vid.title,
            input_message_content=InputTextMessageContent(
                message_text=vid.url,
            ),
            description=f"Dᴜʀᴀᴛɪᴏɴ : {vid.duration}\nVɪᴇᴡs : {vid.views}\nRᴀᴛɪɴɢ : {vid.rating}",
            thumb_url=vid.thumb,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Wᴀᴛᴄʜ Oɴʟɪɴᴇ", url=vid.url),
                InlineKeyboardButton(
                    "Sᴇᴀʀᴄʜ Mᴏʀᴇ", switch_inline_query_current_chat=f"{query}",)
            ]]),
        ))

    await InlineQuery.answer(results, switch_pm_text="Search Results", switch_pm_parameter="start")
