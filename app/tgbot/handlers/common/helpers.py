from typing import NamedTuple, Callable, Optional

from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from states.advanced import LoginState

import texts
from dto.chat_bot import EmailDto, UserIdDto
from services.http_client import HttpChatBot


class Handler(NamedTuple):
    handler: Callable
    filters: list


async def perform_sending_email_code(message: types.Message, state: FSMContext, email: str):
    data = await HttpChatBot.code_to_email(EmailDto(email=email))

    await state.update_data(EmailCode=data.get("Code"))
    await state.update_data(UserId=data.get("UserId"))

    await message.answer("Ми відправили вам код на пошту. Впишіть його будь ласка ⬇️")

    return await state.set_state(LoginState.waiting_code)


async def update_user_state_data(state: FSMContext):
    data = await state.get_data()

    id = data.get("UserId")

    user_params = await HttpChatBot.get_user_params(UserIdDto(user_id=id))

    await state.set_data({"UserId": id, **user_params})


async def send_loading_message(message: types.Message):
    return await message.answer(text=texts.LOADING, reply_markup=ReplyKeyboardRemove())


async def independent_message(text: str, reply_markup: Optional = None, **kwargs):
    message: types.Message = kwargs.get("message")

    if message:
        await message.answer(text=text, reply_markup=reply_markup)
    else:
        bot: Bot = kwargs.get("bot")
        chat_id: int = kwargs.get("chat_id")

        await bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
