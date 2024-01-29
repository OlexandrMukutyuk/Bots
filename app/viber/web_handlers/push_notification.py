import json
import logging
from asyncio import sleep
from typing import Union

from aiohttp import web

import texts
from data import config
from handlers.common.helpers import update_user_state_data
from keyboards.cabinet import cabinet_menu_kb
from services.database import DB
from services.redis import redis_storage
from states import FullCabinetStates
from viber import viber
from viberio.fsm.context import FSMContext
from viberio.fsm.storages.base import StorageKey
from viberio.types import messages
from viberio.types.messages.keyboard_message import Keyboard

ACTIVATE_USER = "KC Activate User"
PUSH_NOTIFICATION = "KC Show Result about Request"


async def push_notification(req: web.Request):
    if req.body_exists:
        data: dict = await req.json()

        api_key = data.get("apikey")

        if api_key == config.APIKEY_FOR_SERVER:
            segment = data.get("segment")
            map = data.get("map")

            if segment is not None and map == ACTIVATE_USER:
                return await register_notification(data)

            if segment is None and map == ACTIVATE_USER:
                return await mass_notification(data)

            if segment is not None and map != ACTIVATE_USER:
                return await single_notification(data)

    return web.Response(text="Bad request", status=400)


async def register_notification(data: dict):
    segment = data.get("segment")
    user_id = int(segment.split("=")[1])
    updated_user_id = data.get("payload").get("user_id")

    user_info = await DB.select_one("SELECT sender_id FROM users WHERE user_id = ?", (user_id,))
    try:
        sender_id = user_info[0]
    except:
        return web.Response(status=200)

    bot_id = config.BOT_TOKEN.split(":")[0]

    state = FSMContext(storage=redis_storage, key=StorageKey(bot_id=bot_id, user_id=sender_id))

    await state.update_data(UserId=updated_user_id)
    await update_user_state_data(state)

    await state.set_state(FullCabinetStates.waiting_menu)

    await viber.send_message(
        sender_id,
        messages.KeyboardMessage(
            text=texts.SUGGEST_HELP, keyboard=cabinet_menu_kb, min_api_version="3"
        ),
    )

    return web.Response(status=200)


async def single_notification(data: dict):
    segment: Union[str, None] = data.get("segment", None)

    user_id = int(segment.split("=")[1])

    user_info = await DB.select_one("SELECT sender_id FROM users WHERE user_id = ?", (user_id,))

    try:
        users = [(user_info[0])]
    except:
        return web.Response(status=200)

    text = data.get("payload").get("result_text_ua")

    for i, user in enumerate(users):
        if i != 0 and i % 20 == 0:
            await sleep(1)

        try:
            await viber.send_message(
                user,
                messages.TextMessage(text=text),
            )
        except:
            logging.warn("Block by user")

    for user in users:
        last_msg = await DB.select_one("SELECT * FROM messages WHERE sender_id = ?", (user,))

        if last_msg is None:
            continue

        text = last_msg[1]
        keyboard_data = last_msg[2]

        if keyboard_data:
            keyboard = Keyboard.from_dict(json.loads(keyboard_data))
            message = messages.KeyboardMessage(text=text, keyboard=keyboard, min_api_version="3")
        else:
            message = messages.TextMessage(text=text)

        try:
            await viber.send_message(
                user,
                message,
            )
        except:
            logging.warn("Block by user")

    return web.Response(status=200)


async def mass_notification(data: dict):
    user_info = await DB.select_all("SELECT sender_id FROM users")
    users = [item for tuple in user_info for item in tuple]

    text = data.get("text")

    for i, user in enumerate(users):
        if i != 0 and i % 20 == 0:
            await sleep(1)

        try:
            await viber.send_message(
                user,
                messages.TextMessage(text=text),
            )
        except:
            logging.warn("Block by user")

    for user in users:
        last_msg = await DB.select_one("SELECT * FROM messages WHERE sender_id = ?", (user,))

        if last_msg is None:
            continue

        text = last_msg[1]
        keyboard_data = last_msg[2]

        if keyboard_data:
            keyboard = Keyboard.from_dict(json.loads(keyboard_data))
            message = messages.KeyboardMessage(text=text, keyboard=keyboard, min_api_version="3")
        else:
            message = messages.TextMessage(text=text)

        try:
            await viber.send_message(
                user,
                message,
            )
        except:
            logging.warn("Block by user")

    return web.Response(status=200)
