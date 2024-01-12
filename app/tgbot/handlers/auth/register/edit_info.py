from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

import texts
from handlers.common import StreetsHandlers, independent_message
from keyboards.default.auth.edit_info import edit_text, edit_register_info_kb
from keyboards.default.auth.register import (
    without_flat_kb,
    phone_share_kb,
    without_flat_text,
)
from keyboards.inline.callbacks import StreetCallbackFactory
from services.http_client import verify_address
from states.auth import EditRegisterState
from utils.template_engine import render_template


async def handle_buttons(message: types.Message, state: FSMContext):
    button_type = message.text

    if button_type == edit_text["first_name_text"]:
        await state.set_state(EditRegisterState.waiting_first_name)
        return await message.answer(
            text=texts.ASKING_FIRST_NAME, reply_markup=ReplyKeyboardRemove()
        )

    if button_type == edit_text["middle_name_text"]:
        await state.set_state(EditRegisterState.waiting_middle_name)
        return await message.answer(
            text=texts.ASKING_MIDDLE_NAME, reply_markup=ReplyKeyboardRemove()
        )

    if button_type == edit_text["last_name_text"]:
        await state.set_state(EditRegisterState.waiting_last_name)
        return await message.answer(
            text=texts.ASKING_LAST_NAME, reply_markup=ReplyKeyboardRemove()
        )

    if button_type == edit_text["phone_text"]:
        await state.set_state(EditRegisterState.waiting_phone)
        await message.answer(text=texts.ASKING_PHONE, reply_markup=phone_share_kb)
        return await message.answer(texts.PHONE_EXAMPLE)

    if button_type == edit_text["password_text"]:
        await state.set_state(EditRegisterState.waiting_password)
        await message.answer(
            text=texts.ASKING_PASSWORD, reply_markup=ReplyKeyboardRemove()
        )

        return await message.answer(texts.PASSWORD_REQS)

    if button_type == edit_text["street_text"]:
        await state.set_state(EditRegisterState.waiting_street_typing)
        return await message.answer(
            text=texts.ASKING_STREET, reply_markup=ReplyKeyboardRemove()
        )

    if button_type == edit_text["house_text"]:
        await state.set_state(EditRegisterState.waiting_house)
        return await message.answer(
            text=texts.ASKING_HOUSE, reply_markup=ReplyKeyboardRemove()
        )

    if button_type == edit_text["flat_text"]:
        await state.set_state(EditRegisterState.waiting_flat)
        return await message.answer(
            text=texts.ASKING_FLAT, reply_markup=without_flat_kb
        )


async def first_time_showing_user_info(message: types.Message, state: FSMContext):
    await send_user_info(state, message=message)


async def send_user_info(state: FSMContext, **kwargs):
    user_data = await state.get_data()

    await state.set_state(EditRegisterState.waiting_accepting)

    info_template = render_template("register/confirming_info.j2", data=user_data)

    await independent_message(text=info_template)
    await independent_message(
        text=texts.IS_EVERYTHING_CORRECT, reply_markup=edit_register_info_kb
    )

    return


async def edit_phone(message: types.Message, state: FSMContext):
    phone = message.text or message.contact.phone_number

    await state.update_data(Phone=phone)
    await state.set_state(EditRegisterState.waiting_accepting)

    await send_user_info(state, message=message)


async def edit_street(message: types.Message, state: FSMContext):
    return await StreetsHandlers.choose_street(
        message, state, EditRegisterState.waiting_street_selected
    )


async def show_street_list(callback: types.InlineQuery, state: FSMContext):
    streets_data = (await state.get_data()).get("Streets")

    return await StreetsHandlers.inline_list(
        callback=callback, streets_data=streets_data
    )


async def confirm_street(
    callback: types.CallbackQuery,
    callback_data: StreetCallbackFactory,
    state: FSMContext,
    bot: Bot,
):
    async def action():
        await state.set_state(EditRegisterState.waiting_accepting)
        await send_user_info(state, bot=bot, chat_id=callback.from_user.id)

    await StreetsHandlers.confirm_street(
        callback=callback, callback_data=callback_data, state=state, action=action
    )


async def edit_house(message: types.Message, state: FSMContext):
    house = message.text

    street_id = (await state.get_data()).get("StreetId")

    is_address_correct = await verify_address(street_id=street_id, house=house)

    if not is_address_correct:
        await message.answer(texts.HOUSE_NOT_FOUND)
        await message.answer(texts.ASKING_HOUSE)
        return

    await state.update_data(House=house)
    await state.set_state(EditRegisterState.waiting_accepting)

    await send_user_info(state, message=message)


async def edit_flat(message: types.Message, state: FSMContext):
    flat = message.text

    if flat == without_flat_text:
        flat = None

    await state.update_data(Flat=flat)
    await state.set_state(EditRegisterState.waiting_accepting)

    await send_user_info(state, message=message)


async def edit_first_name(message: types.Message, state: FSMContext):
    first_name = message.text

    await state.update_data(FirstName=first_name)
    await state.set_state(EditRegisterState.waiting_accepting)

    await send_user_info(state, message=message)


async def edit_middle_name(message: types.Message, state: FSMContext):
    middle_name = message.text

    await state.update_data(MiddleName=middle_name)
    await state.set_state(EditRegisterState.waiting_accepting)

    await send_user_info(state, message=message)


async def edit_last_name(message: types.Message, state: FSMContext):
    last_name = message.text

    await state.update_data(LastName=last_name)
    await state.set_state(EditRegisterState.waiting_accepting)

    await send_user_info(state, message=message)


async def edit_password(message: types.Message, state: FSMContext):
    await state.update_data(Password=message.text)
    await state.set_state(EditRegisterState.waiting_accepting)

    await send_user_info(state, message=message)


async def accept_info(message: types.Message, state: FSMContext):
    data = await state.get_data()

    # TODO Register auth
    for key, value in data.items():
        print(f"{key}: {value}")

    await message.answer("Ми відправили посилання вам на пошту. Перейдіть по ньому")
    await message.answer(
        "(Треба сервер, щоб доробити реєстрацію, зараз працювати не буде)",
        reply_markup=ReplyKeyboardRemove(),
    )
