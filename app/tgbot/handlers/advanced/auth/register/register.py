from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

import texts
from dto.chat_bot import PhoneDto
from handlers.common.flat import FlatHandlers
from handlers.common.house import HouseHandlers
from handlers.common.streets import StreetsHandlers
from keyboards.default.auth.register import (
    choose_gender_kb,
    registration_agreement_kb, phone_share_kb,
)
from keyboards.default.common import change_street_kb, without_flat_kb
from keyboards.inline.callbacks import StreetCallbackFactory
from models import Gender
from services.http_client import HttpChatBot
from states.advanced import AdvancedRegisterStates
from utils.template_engine import render_template


async def save_phone(message: types.Message, state: FSMContext):
    phone = message.text or message.contact.phone_number

    unique_phone = await HttpChatBot.unique_phone(PhoneDto(phone=phone))
    if not unique_phone:
        await message.answer(texts.UNIQUE_PHONE)
        await message.answer(texts.ASKING_PHONE, reply_markup=phone_share_kb)
        return

    await state.update_data(Phone=phone)
    await message.answer("Ваш номер успішно відправлено")

    await state.set_state(AdvancedRegisterStates.waiting_street_typing)
    await message.answer(text=texts.ASKING_STREET, reply_markup=ReplyKeyboardRemove())


async def choose_street(message: types.Message, state: FSMContext, bot: Bot):
    return await StreetsHandlers.choose_street(
        message, state, AdvancedRegisterStates.waiting_street_selected, bot
    )


async def show_street_list(callback: types.InlineQuery, state: FSMContext):
    streets_data = (await state.get_data()).get("Streets")

    return await StreetsHandlers.inline_list(callback, streets_data)


async def confirm_street(
        callback: types.CallbackQuery, callback_data: StreetCallbackFactory, state: FSMContext, bot: Bot
):
    async def action():
        await bot.send_message(
            chat_id=callback.from_user.id, text=texts.ASKING_HOUSE, reply_markup=change_street_kb
        )
        await state.set_state(AdvancedRegisterStates.waiting_house)

    await StreetsHandlers.confirm_street(
        callback=callback, callback_data=callback_data, state=state, action=action, bot=bot
    )


async def change_street(message: types.Message, state: FSMContext):
    await state.set_state(AdvancedRegisterStates.waiting_street_typing)
    await message.answer(text=texts.ASKING_STREET, reply_markup=ReplyKeyboardRemove())


async def save_house(message: types.Message, state: FSMContext):
    async def callback():
        await message.answer(text=texts.ASKING_FLAT, reply_markup=without_flat_kb)

    await HouseHandlers.change_house(
        message=message,
        state=state,
        new_state=AdvancedRegisterStates.waiting_flat,
        callback=callback,
    )


async def save_flat(message: types.Message, state: FSMContext):
    async def callback():
        await message.answer(text=texts.ASKING_FIRST_NAME, reply_markup=ReplyKeyboardRemove())

    return await FlatHandlers.change_flat(
        message=message,
        state=state,
        new_state=AdvancedRegisterStates.waiting_first_name,
        callback=callback,
    )


async def save_first_name(message: types.Message, state: FSMContext):
    first_name = message.text

    await state.update_data(FirstName=first_name)
    await state.set_state(AdvancedRegisterStates.waiting_middle_name)

    return await message.answer(texts.ASKING_LAST_NAME)


async def save_middle_name(message: types.Message, state: FSMContext):
    middle_name = message.text

    await state.update_data(MiddleName=middle_name)
    await state.set_state(AdvancedRegisterStates.waiting_last_name)

    return await message.answer(texts.ASKING_MIDDLE_NAME)


async def save_last_name(message: types.Message, state: FSMContext):
    last_name = message.text

    await state.update_data(LastName=last_name)
    await state.set_state(AdvancedRegisterStates.waiting_gender)

    return await message.answer(text=texts.ASKING_GENDER, reply_markup=choose_gender_kb)


async def save_gender(message: types.Message, state: FSMContext):
    print(message.text)

    gender = Gender.get_key(message.text)
    await state.update_data(Gender=gender)
    await state.set_state(AdvancedRegisterStates.waiting_password)

    await message.answer(texts.ASKING_PASSWORD)
    await message.answer(texts.PASSWORD_REQS)

    return


async def save_password(message: types.Message, state: FSMContext):
    await state.update_data(Password=message.text)
    await state.set_state(AdvancedRegisterStates.waiting_agreement)

    return await show_agreement(message)


async def show_agreement(message: types.Message):
    return await message.answer(
        text=render_template("register/agreement.j2"), reply_markup=registration_agreement_kb
    )
