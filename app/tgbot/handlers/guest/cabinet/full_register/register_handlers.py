from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

import texts
from handlers.common.flat import FlatHandlers
from keyboards.default.auth.register import (
    choose_gender_kb,
    registration_agreement_kb,
)
from keyboards.default.common import without_flat_kb
from models import Gender
from states import GuestFullRegisterStates
from utils.template_engine import render_template


async def save_phone(message: types.Message, state: FSMContext):
    phone = message.text or message.contact.phone_number

    await state.update_data(Phone=phone)
    await message.answer(texts.GOT_PHONE)

    await state.set_state(GuestFullRegisterStates.waiting_flat)
    await message.answer(text=texts.ASKING_FLAT, reply_markup=without_flat_kb)


async def save_flat(message: types.Message, state: FSMContext):
    async def callback():
        await message.answer(text=texts.ASKING_FIRST_NAME, reply_markup=ReplyKeyboardRemove())

    return await FlatHandlers.change_flat(
        message=message,
        state=state,
        new_state=GuestFullRegisterStates.waiting_first_name,
        callback=callback,
    )


async def save_first_name(message: types.Message, state: FSMContext):
    first_name = message.text

    await state.update_data(FirstName=first_name)
    await state.set_state(GuestFullRegisterStates.waiting_middle_name)

    return await message.answer(texts.ASKING_LAST_NAME)


async def save_middle_name(message: types.Message, state: FSMContext):
    middle_name = message.text

    await state.update_data(MiddleName=middle_name)
    await state.set_state(GuestFullRegisterStates.waiting_last_name)

    return await message.answer(texts.ASKING_MIDDLE_NAME)


async def save_last_name(message: types.Message, state: FSMContext):
    last_name = message.text

    await state.update_data(LastName=last_name)
    await state.set_state(GuestFullRegisterStates.waiting_gender)

    return await message.answer(text=texts.ASKING_GENDER, reply_markup=choose_gender_kb)


async def save_gender(message: types.Message, state: FSMContext):
    gender = Gender.get_key(message.text)
    await state.update_data(Gender=gender)
    await state.set_state(GuestFullRegisterStates.waiting_password)

    await message.answer(texts.ASKING_PASSWORD)
    await message.answer(texts.PASSWORD_REQS)

    return


async def save_password(message: types.Message, state: FSMContext):
    await state.update_data(Password=message.text)
    await state.set_state(GuestFullRegisterStates.waiting_agreement)

    return await show_agreement(message)


async def show_agreement(message: types.Message):
    return await message.answer(
        text=render_template("register/agreement.j2"), reply_markup=registration_agreement_kb
    )
