import logging

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hlink
from aiohttp import ContentTypeError

import texts
from data.config import WEBSITE_URL
from dto.chat_bot import CheckEmailDto
from handlers.common.helpers import send_loading_message, perform_sending_email_code
from keyboards.default.auth.register import phone_share_kb
from keyboards.default.basic import yes_n_no
from keyboards.default.start import greeting_kb, auth_types_kb
from keyboards.default.start import is_register_on_site, start_again_kb, yes_text, no_text
from services.http_client import HttpChatBot
from states.advanced import AuthState, RegisterState
from states.start import StartState
from states.subscription import AuthStates


async def greeting(message: types.Message, state: FSMContext):
    await state.clear()

    await message.answer(text=texts.GREETING, reply_markup=greeting_kb)
    await state.set_state(StartState.waiting_greeting)


async def introduction(message: types.Message, state: FSMContext):
    await message.answer(texts.INTRODUCTION)
    await message.answer(text=texts.PICK_AUTH_TYPE, reply_markup=auth_types_kb)
    await message.answer(texts.ADVANCED_INFO)
    await message.answer(texts.SUBSCRIPTION_INFO)

    await state.set_state(StartState.waiting_auth_type)


async def check_user_email(message: types.Message, state: FSMContext):
    email = message.text

    await state.update_data(Email=email)

    loading = await send_loading_message(message=message)

    try:
        is_user_exist = await HttpChatBot.check_email(CheckEmailDto(email=email))
    except ContentTypeError as e:
        logging.error(e)
        return await message.answer(texts.SERVER_ERROR)

    await loading.delete()

    if is_user_exist:
        return await perform_sending_email_code(message, state, email)

    await asking_if_register(message, state)


async def answer_if_register(message: types.Message, state: FSMContext):
    message_text = message.text

    if message_text == yes_text:
        await asking_if_email_confirmed(message, state)

    if message_text == no_text:
        await message.answer(texts.NEED_REGISTER)
        await message.answer(text=texts.ASKING_PHONE, reply_markup=phone_share_kb)
        await message.answer(texts.PHONE_EXAMPLE)
        await state.set_state(RegisterState.waiting_phone)


async def answer_if_confirmed_email(message: types.Message):
    message_text = message.text

    if message_text == yes_text:
        await message.answer(text=texts.CALL_SUPPORT, reply_markup=start_again_kb)

    if message_text == no_text:
        link = hlink("Посилання на наш сайт", WEBSITE_URL)

        await message.answer(
            text=f"Щоб продовжити користуватися чат-ботом, вам потрібно підтвердити ваш e-mail\n\n{link}",
            reply_markup=start_again_kb,
        )


async def start_again(message: types.Message, state: FSMContext):
    await state.update_data(Email=None)

    await asking_email(message, state)


async def asking_email(message: types.Message, state: FSMContext):
    await message.answer(text=texts.ASKING_EMAIL, reply_markup=ReplyKeyboardRemove())
    await state.set_state(AuthState.waiting_email)


async def asking_if_register(message: types.Message, state: FSMContext):
    await message.answer(text=texts.IS_REGISTER_ON_SITE, reply_markup=is_register_on_site)
    await state.set_state(AuthState.answering_if_register)


async def asking_if_email_confirmed(message: types.Message, state: FSMContext):
    await state.set_state(AuthState.answering_if_confirmed_email)
    await message.answer(text=texts.IS_EMAIL_CONFIRMED, reply_markup=yes_n_no)


async def subscription_auth(message: types.Message, state: FSMContext):
    await message.answer(text=texts.ASKING_STREET, reply_markup=ReplyKeyboardRemove())

    await state.set_state(AuthStates.waiting_street_typing)
