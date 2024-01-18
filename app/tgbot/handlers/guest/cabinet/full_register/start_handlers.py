from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

import texts
from data.config import WEBSITE_URL
from handlers.common.email import EmailHandlers
from keyboards.default.auth.register import phone_share_kb
from keyboards.default.basic import yes_n_no
from keyboards.default.start import start_again_kb, is_register_on_site
from states import GuestFullRegisterStates
from texts import YES, NO
from utils.template_engine import render_template


async def asking_email(message: types.Message, state: FSMContext):
    await message.answer(text=texts.ASKING_EMAIL, reply_markup=ReplyKeyboardRemove())
    await state.set_state(GuestFullRegisterStates.waiting_email)


async def check_user_email(message: types.Message, state: FSMContext):
    async def action():
        return await asking_if_register(message, state)

    await EmailHandlers.check_user(
        message=message,
        state=state,
        exist_state=GuestFullRegisterStates.waiting_code,
        action=action,
    )


async def check_email_code(message: types.Message, state: FSMContext):
    async def action():
        return await start_again(message, state)

    await EmailHandlers.check_code(
        message=message,
        state=state,
        failure_state=GuestFullRegisterStates.waiting_code,
        other_email_action=action,
    )


async def answer_if_register(message: types.Message, state: FSMContext):
    message_text = message.text

    if message_text == YES:
        await asking_if_email_confirmed(message, state)

    if message_text == NO:
        await message.answer(text=texts.NEED_REGISTER)
        await message.answer(text=texts.ASKING_PHONE, reply_markup=phone_share_kb)
        await message.answer(text=texts.PHONE_EXAMPLE)
        await state.set_state(GuestFullRegisterStates.waiting_phone)


async def answer_if_confirmed_email(message: types.Message):
    message_text = message.text

    if message_text == YES:
        await message.answer(text=texts.CALL_SUPPORT, reply_markup=start_again_kb)

    if message_text == NO:
        await message.answer(
            text=render_template("website_link.j2", url=WEBSITE_URL),
            reply_markup=start_again_kb,
        )


async def start_again(message: types.Message, state: FSMContext):
    await state.update_data(Email=None)

    await asking_email(message, state)


async def asking_if_register(message: types.Message, state: FSMContext):
    await message.answer(text=texts.IS_REGISTER_ON_SITE, reply_markup=is_register_on_site)
    await state.set_state(GuestFullRegisterStates.answering_if_register)


async def asking_if_email_confirmed(message: types.Message, state: FSMContext):
    await state.set_state(GuestFullRegisterStates.answering_if_confirmed_email)
    await message.answer(text=texts.IS_EMAIL_CONFIRMED, reply_markup=yes_n_no)
