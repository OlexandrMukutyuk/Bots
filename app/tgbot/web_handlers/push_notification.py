import logging
from asyncio import sleep
from typing import Union

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiohttp import web

from bot import bot
from data import config
from handlers.common.helpers import full_cabinet_menu
from services.database import DB
from services.redis import redis_storage

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

    user_id = int(segment.split("=")[1])

    user_info = await DB.select_one("SELECT sender_id FROM users WHERE user_id = ?", (user_id,))
    chat_id = user_info[0]

    bot_id = int(config.BOT_TOKEN.split(':')[0])

    state = FSMContext(storage=redis_storage, key=StorageKey(chat_id=chat_id, bot_id=bot_id, user_id=chat_id))

    await full_cabinet_menu(state, bot=bot, chat_id=chat_id)

    return web.Response(status=200)


async def notification(data: dict):
    segment: Union[str, None] = data.get('segment', None)

    if not segment:
        user_info = await DB.select_all("SELECT sender_id FROM users")
        users = [item for tuple in user_info for item in tuple]
    else:
        user_id = int(segment.split("=")[1])

        user_info = await DB.select_one("SELECT sender_id FROM users WHERE user_id = ?", (user_id,))

        users = [(user_info[0])]

    text = data.get('payload').get('result_text_ua')

    for i, user in enumerate(users):

        if i != 0 and i % 20 == 0:
            await sleep(1)

        try:
            await bot.send_message(chat_id=user, text=text)
        except:
            logging.warn("Block by user")

    # for user in users:
    #     last_msg = await DB.select_one("SELECT * FROM messages WHERE sender_id = ?", (user,))
    #
    #     if last_msg is None:
    #         continue
    #
    #     text = last_msg[1]
    #     keyboard_data = last_msg[2]
    #
    #     if keyboard_data:
    #         keyboard = Keyboard.from_dict(json.loads(keyboard_data))
    #         message = messages.KeyboardMessage(text=text, keyboard=keyboard, min_api_version='3')
    #     else:
    #         message = messages.TextMessage(text=text)
    #
    #     try:
    #         await viber.send_message(
    #             user,
    #             message,
    #         )
    #     except:
    #         logging.warn("Block by user")

    return web.Response(status=200)
