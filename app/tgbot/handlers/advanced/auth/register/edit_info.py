import json

from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

import texts
from bot import redis_pool
from dto.chat_bot import RegisterDto
from handlers.common.flat import FlatHandlers
from handlers.common.helpers import independent_message
from handlers.common.house import HouseHandlers
from handlers.common.streets import StreetsHandlers
from keyboards.default.auth.edit_info import edit_text, edit_register_info_kb
from keyboards.default.auth.login import other_email_kb
from keyboards.default.auth.register import (
    phone_share_kb,
)
from keyboards.default.common import without_flat_kb
from keyboards.inline.callbacks import StreetCallbackFactory
from services.http_client import HttpChatBot
from states.advanced import EditRegisterStates
from utils.template_engine import render_template


async def handle_buttons(message: types.Message, state: FSMContext):
    button_type = message.text

    if button_type == edit_text["first_name_text"]:
        await state.set_state(EditRegisterStates.waiting_first_name)
        return await message.answer(
            text=texts.ASKING_FIRST_NAME, reply_markup=ReplyKeyboardRemove()
        )

    if button_type == edit_text["middle_name_text"]:
        await state.set_state(EditRegisterStates.waiting_middle_name)
        return await message.answer(
            text=texts.ASKING_MIDDLE_NAME, reply_markup=ReplyKeyboardRemove()
        )

    if button_type == edit_text["last_name_text"]:
        await state.set_state(EditRegisterStates.waiting_last_name)
        return await message.answer(text=texts.ASKING_LAST_NAME, reply_markup=ReplyKeyboardRemove())

    if button_type == edit_text["phone_text"]:
        await state.set_state(EditRegisterStates.waiting_phone)
        await message.answer(text=texts.ASKING_PHONE, reply_markup=phone_share_kb)
        return await message.answer(texts.PHONE_EXAMPLE)

    if button_type == edit_text["password_text"]:
        await state.set_state(EditRegisterStates.waiting_password)
        await message.answer(text=texts.ASKING_PASSWORD, reply_markup=ReplyKeyboardRemove())

        return await message.answer(texts.PASSWORD_REQS)

    if button_type == edit_text["street_text"]:
        await state.set_state(EditRegisterStates.waiting_street_typing)
        return await message.answer(text=texts.ASKING_STREET, reply_markup=ReplyKeyboardRemove())

    if button_type == edit_text["house_text"]:
        await state.set_state(EditRegisterStates.waiting_house)
        return await message.answer(text=texts.ASKING_HOUSE, reply_markup=ReplyKeyboardRemove())

    if button_type == edit_text["flat_text"]:
        await state.set_state(EditRegisterStates.waiting_flat)
        return await message.answer(text=texts.ASKING_FLAT, reply_markup=without_flat_kb)

    if button_type == edit_text["accept_info_text"]:
        return await accept_info(message, state)


async def first_time_showing_user_info(message: types.Message, state: FSMContext):
    await send_user_info(state, message=message)


async def send_user_info(state: FSMContext, **kwargs):
    user_data = await state.get_data()

    await state.set_state(EditRegisterStates.waiting_accepting)

    info_template = render_template("register/confirming_info.j2", data=user_data)

    await independent_message(text=info_template, **kwargs)
    await independent_message(
        text=texts.IS_EVERYTHING_CORRECT, reply_markup=edit_register_info_kb, **kwargs
    )


async def edit_phone(message: types.Message, state: FSMContext):
    phone = message.text or message.contact.phone_number

    await state.update_data(Phone=phone)
    await state.set_state(EditRegisterStates.waiting_accepting)

    await send_user_info(state, message=message)


async def edit_street(message: types.Message, state: FSMContext, bot: Bot):
    return await StreetsHandlers.choose_street(
        message=message, state=state, new_state=EditRegisterStates.waiting_street_selected, bot=bot
    )


async def show_street_list(callback: types.InlineQuery, state: FSMContext):
    streets_data = (await state.get_data()).get("Streets")

    return await StreetsHandlers.inline_list(callback=callback, streets_data=streets_data)


async def confirm_street(
        callback: types.CallbackQuery,
        callback_data: StreetCallbackFactory,
        state: FSMContext,
        bot: Bot,
):
    async def action():
        await state.set_state(EditRegisterStates.waiting_house)
        await independent_message(
            text=texts.ASKING_HOUSE,
            reply_markup=ReplyKeyboardRemove(),
            bot=bot,
            chat_id=callback.from_user.id,
        )

    await StreetsHandlers.confirm_street(
        callback=callback, callback_data=callback_data, state=state, action=action, bot=bot
    )


async def edit_house(message: types.Message, state: FSMContext):
    async def callback():
        await send_user_info(state, message=message)

    return await HouseHandlers.change_house(
        message=message,
        state=state,
        new_state=EditRegisterStates.waiting_accepting,
        callback=callback,
    )


async def edit_flat(message: types.Message, state: FSMContext):
    async def callback():
        await send_user_info(state, message=message)

    await FlatHandlers.change_flat(
        message=message,
        state=state,
        new_state=EditRegisterStates.waiting_accepting,
        callback=callback,
    )


async def edit_first_name(message: types.Message, state: FSMContext):
    first_name = message.text

    await state.update_data(FirstName=first_name)
    await state.set_state(EditRegisterStates.waiting_accepting)

    await send_user_info(state, message=message)


async def edit_middle_name(message: types.Message, state: FSMContext):
    middle_name = message.text

    await state.update_data(MiddleName=middle_name)
    await state.set_state(EditRegisterStates.waiting_accepting)

    await send_user_info(state, message=message)


async def edit_last_name(message: types.Message, state: FSMContext):
    last_name = message.text

    await state.update_data(LastName=last_name)
    await state.set_state(EditRegisterStates.waiting_accepting)

    await send_user_info(state, message=message)


async def edit_password(message: types.Message, state: FSMContext):
    await state.update_data(Password=message.text)
    await state.set_state(EditRegisterStates.waiting_accepting)

    await send_user_info(state, message=message)


async def accept_info(message: types.Message, state: FSMContext):
    data = await state.get_data()

    user_id = await HttpChatBot.register(
        RegisterDto(
            first_name=data.get("FirstName"),
            last_name=data.get("LastName"),
            middle_name=data.get("MiddleName"),
            gender=data.get("Gender"),
            phone=data.get("Phone"),
            city_id=data.get("CityId"),
            street_id=data.get("StreetId"),
            house=data.get("House"),
            flat=data.get("Flat"),
            password=data.get("Password"),
            email=data.get("Email"),
        )
    )

    users = json.loads(await redis_pool.get('users'))

    await redis_pool.set('users', json.dumps({
        **users,
        message.from_user.id: user_id
    }))

    await state.update_data(UserId=user_id)

    await state.set_state(EditRegisterStates.waiting_email_confirming)

    await message.answer("Інформація для реєстрації відправлена успішно!")
    await message.answer(
        "Будь ласка, підтвердіть свою пошту (перейдіть за посиланням, яке ми вам відправили)"
    )
    await message.answer("Якщо лист не отримано - перевірте спам.", reply_markup=other_email_kb)
