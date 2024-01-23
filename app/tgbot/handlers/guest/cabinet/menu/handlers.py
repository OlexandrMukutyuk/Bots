from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

import texts
from dto.guest import GuestIdDto
from handlers.common.enterprises import EnterprisesHandlers
from handlers.common.helpers import independent_message
from handlers.common.reference_info import ReferenceInfoHandlers
from keyboards.default.guest.auth import (
    subscription_menu_kb,
    guest_menu_text,
    full_registration_kb,
)
from keyboards.default.guest.edit_info import edit_guest_kb
from keyboards.inline.cabinet.cabinet import share_chatbot_kb
from services.http_client import HttpGuestBot
from states.guest import (
    GuestCabinetStates,
    GuestShareBotStates,
    GuestRateEnterpriseStates,
    GuestFullRegisterStates,
    GuestEditInfoStates, ReferenceInfoStates, )
from utils.template_engine import render_template


async def show_cabinet_menu(message: types.Message, state: FSMContext):
    return await give_cabinet_menu(state=state, message=message)


async def give_cabinet_menu(state: FSMContext, **kwargs):
    await state.set_state(GuestCabinetStates.waiting_menu)

    return await independent_message(
        text=texts.SUGGEST_HELP, reply_markup=subscription_menu_kb, **kwargs
    )


async def main_handler(message: types.Message, state: FSMContext):
    button_text = message.text

    if button_text == guest_menu_text["share_chatbot"]:
        return await share_chatbot(message, state)

    if button_text == guest_menu_text["review_enterprises"]:
        return await rate_enterprises_list(message, state)

    if button_text == guest_menu_text["change_info"]:
        return await change_user_info(message, state)

    if button_text == guest_menu_text["full_registration"]:
        return await full_registration(message, state)

    if button_text == guest_menu_text["reference_info"]:
        return await reference_info(message, state)


async def share_chatbot(message: types.Message, state: FSMContext):
    await message.answer(text=texts.SHARE_BOT, reply_markup=ReplyKeyboardRemove())
    await message.answer(text=texts.USE_BUTTONS, reply_markup=share_chatbot_kb)

    return await state.set_state(GuestShareBotStates.waiting_back)


async def rate_enterprises_list(message: types.Message, state: FSMContext):
    async def get_enterprises():
        guest_id = (await state.get_data()).get("GuestId")
        return await HttpGuestBot.get_enterprises(GuestIdDto(guest_id=guest_id))

    async def menu_callback():
        return await give_cabinet_menu(state=state, message=message)

    return await EnterprisesHandlers.enterprises_list(
        message=message,
        state=state,
        get_enterprises=get_enterprises,
        new_state=GuestRateEnterpriseStates.showing_list,
        menu_callback=menu_callback,
    )


async def reference_info(message: types.Message, state: FSMContext):
    await ReferenceInfoHandlers.load_menu(
        state=state,
        parent_id=None,
        new_state=ReferenceInfoStates.waiting_info,
        message=message
    )


async def change_user_info(message: types.Message, state: FSMContext):
    return await send_edit_guest_info(state, message=message)


async def send_edit_guest_info(state: FSMContext, **kwargs):
    user_data = await state.get_data()

    data = {
        "Street": user_data.get("Street"),
        "House": user_data.get("House"),
    }

    template = render_template("edit_guest_info.j2", data=data)

    await state.set_state(GuestEditInfoStates.waiting_acceptation)
    return await independent_message(template, edit_guest_kb, **kwargs)


async def full_registration(message: types.Message, state: FSMContext):
    await state.set_state(GuestFullRegisterStates.waiting_answer)
    await message.answer(text=texts.FULL_REGISTER_INFO, reply_markup=full_registration_kb)


# Back button handlers

async def to_main_menu_inline(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.delete()

    return await give_cabinet_menu(state, bot=bot, chat_id=callback.from_user.id)


async def to_main_menu_reply(message: types.Message, state: FSMContext):
    await message.delete()

    return await give_cabinet_menu(state=state, message=message)
