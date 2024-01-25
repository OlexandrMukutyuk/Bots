import json
import logging
from asyncio import sleep
from typing import Union

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiohttp import web

from bot import bot, redis_pool, redis_storage
from data import config
from handlers.common.helpers import full_cabinet_menu

ACTIVATE_USER = "Activate User"
PUSH_NOTIFICATION = "Push Notification"


async def push_notification(req: web.Request):
    if req.body_exists:
        data: dict = await req.json()

        api_key = data.get('apiKey')

        if api_key == config.APIKEY_FOR_SERVER:
            if data.get('map') == ACTIVATE_USER:
                return await register_notification(data)
            else:
                return await notification(data)

    return web.Response(text="Bad request", status=400)


async def register_notification(data: dict):
    segment: Union[str, None] = data.get('segment', None)

    if not segment:
        return web.Response(status=400)

    users_info = json.loads(await redis_pool.get('users'))

    user_id = int(segment.split('=')[1])

    user_info = {key: value for key, value in users_info.items() if value == user_id}

    chat_id = list(user_info.keys())[0]
    bot_id = int(config.BOT_TOKEN.split(':')[0])

    state = FSMContext(storage=redis_storage, key=StorageKey(chat_id=chat_id, bot_id=bot_id, user_id=chat_id))

    await full_cabinet_menu(state, bot=bot, chat_id=chat_id)

    return web.Response(status=200)


async def notification(data: dict):
    segment: Union[str, None] = data.get('segment', None)

    users_info = json.loads(await redis_pool.get('users'))

    if not segment:
        users = list(users_info.keys())
    else:
        user_id = int(segment.split('=')[1])
        user_info = {key: value for key, value in users_info.items() if value == user_id}

        users = list(user_info.keys())

    text = data.get('payload').get('result_text_ua')

    for i, user in enumerate(users):

        if i != 0 and i % 20 == 0:
            await sleep(1)

        try:
            await bot.send_message(chat_id=user, text=text)
        except:
            logging.warn("Block by user")

    return web.Response(status=200)
