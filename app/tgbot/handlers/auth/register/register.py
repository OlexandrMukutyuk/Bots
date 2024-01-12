from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

import texts
from handlers.common import StreetsHandlers
from keyboards.default.auth.register import (
    change_street_kb,
    without_flat_kb,
    without_flat_text,
    choose_gender_kb, gender_dict, registration_agreement_kb
)
from keyboards.inline.callbacks import StreetCallbackFactory
from services.http_client import verify_address
from states.auth import AdvancedRegisterState
from utils.template_engine import render_template


async def save_phone(message: types.Message, state: FSMContext):
    phone = message.text or message.contact.phone_number

    await state.update_data(Phone=phone)
    await message.answer("Ваш номер успішно відправлено")

    await state.set_state(AdvancedRegisterState.waiting_street_typing)
    await message.answer(
        text=texts.ASKING_STREET,
        reply_markup=ReplyKeyboardRemove()
    )


async def choose_street(message: types.Message, state: FSMContext):
    return await StreetsHandlers.choose_street(message, state, AdvancedRegisterState.waiting_street_selected)


async def show_street_list(callback: types.InlineQuery, state: FSMContext):
    streets_data = (await state.get_data()).get('Streets')

    return await StreetsHandlers.inline_list(callback, streets_data)


async def confirm_street(
        callback: types.CallbackQuery,
        callback_data: StreetCallbackFactory,
        state: FSMContext,
        bot: Bot
):
    async def action():
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=texts.ASKING_HOUSE,
            reply_markup=change_street_kb
        )
        await state.set_state(AdvancedRegisterState.waiting_house)

    await StreetsHandlers.confirm_street(
        callback=callback,
        callback_data=callback_data,
        state=state,
        action=action
    )


async def change_street(message: types.Message, state: FSMContext):
    await state.set_state(AdvancedRegisterState.waiting_street_typing)
    await message.answer(
        text=texts.ASKING_STREET,
        reply_markup=ReplyKeyboardRemove()
    )


async def save_house(message: types.Message, state: FSMContext):
    house = message.text

    street_id = (await state.get_data())["StreetId"]

    is_address_correct = await verify_address(street_id=street_id, house=house)

    if not is_address_correct:
        await message.answer(texts.HOUSE_NOT_FOUND)
        return await message.answer(
            text=texts.ASKING_HOUSE,
            reply_markup=change_street_kb
        )

    await state.update_data(House=house)

    await state.set_state(AdvancedRegisterState.waiting_flat)

    await message.answer(
        text=texts.ASKING_FLAT,
        reply_markup=without_flat_kb
    )


async def save_flat(message: types.Message, state: FSMContext):
    flat = message.text

    if flat == without_flat_text:
        flat = None

    await state.update_data(Flat=flat)
    await state.set_state(AdvancedRegisterState.waiting_first_name)

    return await message.answer(
        text=texts.ASKING_FIRST_NAME,
        reply_markup=None)


async def save_first_name(message: types.Message, state: FSMContext):
    first_name = message.text

    await state.update_data(FirstName=first_name)
    await state.set_state(AdvancedRegisterState.waiting_middle_name)

    return await message.answer(texts.ASKING_LAST_NAME)


async def save_middle_name(message: types.Message, state: FSMContext):
    middle_name = message.text

    await state.update_data(MiddleName=middle_name)
    await state.set_state(AdvancedRegisterState.waiting_last_name)

    return await message.answer(texts.ASKING_MIDDLE_NAME)


async def save_last_name(message: types.Message, state: FSMContext):
    last_name = message.text

    await state.update_data(LastName=last_name)
    await state.set_state(AdvancedRegisterState.waiting_gender)

    return await message.answer(
        text=texts.ASKING_GENDER,
        reply_markup=choose_gender_kb
    )


async def save_gender(message: types.Message, state: FSMContext):
    gender = message.text

    if gender == gender_dict['other']:
        gender = None

    await state.update_data(Gender=gender)
    await state.set_state(AdvancedRegisterState.waiting_password)

    await message.answer(texts.ASKING_PASSWORD)
    await message.answer(texts.PASSWORD_REQS)

    return


async def save_password(message: types.Message, state: FSMContext):
    await state.update_data(Password=message.text)
    await state.set_state(AdvancedRegisterState.waiting_agreement)

    return await show_agreement(message)


async def show_agreement(message: types.Message):
    return await message.answer(
        text=render_template('register/agreement.j2'),
        reply_markup=registration_agreement_kb
    )
