from typing import NamedTuple, Callable, Optional

from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

import texts
from dto.chat_bot import UserIdDto
from keyboards.default.cabinet.menu import cabinet_menu_kb
from services.http_client import HttpChatBot
from states import FullCabinetStates


class Handler(NamedTuple):
    handler: Callable
    filters: list


async def full_cabinet_menu(state: FSMContext, **kwargs: object) -> object:
    await state.set_state(FullCabinetStates.waiting_menu)

    return await independent_message(
        text=texts.SUGGEST_HELP, reply_markup=cabinet_menu_kb, **kwargs
    )


async def update_user_state_data(state: FSMContext):
    data = await state.get_data()

    id = data.get("UserId")

    user_params = await HttpChatBot.get_user_params(UserIdDto(user_id=id))

    for key in user_params:
        if user_params[key] in ["", "0"]:
            user_params[key] = None

    await state.set_data({"UserId": id, **user_params})


async def update_guest_state_data(state: FSMContext):
    data = await state.get_data()

    await state.set_data({
        "Street": data.get('Street'),
        "City": data.get('City'),
        "StreetId": data.get('StreetId'),
        "CityId": data.get('CityId'),
        "House": data.get('House'),
        "GuestId": data.get('GuestId')
    })


async def send_loading_message(**kwargs):
    return await independent_message(
        text=texts.LOADING, reply_markup=ReplyKeyboardRemove(), **kwargs
    )


async def independent_message(text: str, reply_markup: Optional = None, **kwargs):
    message: types.Message = kwargs.get("message")

    if message:
        return await message.answer(text=text, reply_markup=reply_markup)
    else:
        bot: Bot = kwargs.get("bot")
        chat_id: int = kwargs.get("chat_id")

        return await bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
