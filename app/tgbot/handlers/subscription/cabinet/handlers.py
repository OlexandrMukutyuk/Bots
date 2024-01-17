from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

import texts
from dto.guest import GuestIdDto
from handlers.common.enterprises import EnterprisesHandlers
from handlers.common.helpers import independent_message
from keyboards.default.cabinet.edit_profile import edit_profile_kb
from keyboards.default.subscription.subscription import subscription_menu_kb, subscription_menu_text
from keyboards.inline.cabinet.cabinet import share_chatbot_kb
from models import Gender
from services.http_client import HttpGuestBot
from states.cabinet import EditInfo
from states.subscription import SubscribeCabinet, SubscribeShareBot, SubscribeRateEnterprise
from utils.template_engine import render_template


async def show_cabinet_menu(message: types.Message, state: FSMContext):
    return await give_cabinet_menu(state=state, message=message)


async def give_cabinet_menu(state: FSMContext, **kwargs):
    await state.set_state(SubscribeCabinet.waiting_menu)

    return await independent_message(
        text=texts.SUGGEST_HELP, reply_markup=subscription_menu_kb, **kwargs
    )


async def main_handler(message: types.Message, state: FSMContext):
    button_text = message.text

    if button_text == subscription_menu_text["share_chatbot"]:
        return await share_chatbot(message, state)

    if button_text == subscription_menu_text["review_enterprises"]:
        return await rate_enterprises(message, state)

    if button_text == subscription_menu_text["change_user_info"]:
        return await change_user_info(message, state)


async def share_chatbot(message: types.Message, state: FSMContext):
    await message.answer(text=texts.SHARE_BOT, reply_markup=ReplyKeyboardRemove())
    await message.answer(text=texts.USE_BUTTONS, reply_markup=share_chatbot_kb)

    return await state.set_state(SubscribeShareBot.waiting_back)


async def rate_enterprises(message: types.Message, state: FSMContext):
    async def get_enterprises():
        guest_id = (await state.get_data()).get("GuestId")
        return await HttpGuestBot.get_enterprises(GuestIdDto(guest_id=guest_id))

    async def menu_callback():
        return await give_cabinet_menu(state=state, message=message)

    return await EnterprisesHandlers.enterprises_list(
        message=message,
        state=state,
        get_enterprises=get_enterprises,
        new_state=SubscribeRateEnterprise.showing_list,
        menu_callback=menu_callback,
    )


async def change_user_info(message: types.Message, state: FSMContext):
    return await send_edit_user_info(state, message=message)


async def send_edit_user_info(state: FSMContext, **kwargs):
    user_data = await state.get_data()

    data = {
        "FirstName": user_data.get("FirstName"),
        "LastName": user_data.get("LastName"),
        "MiddleName": user_data.get("MiddleName"),
        "Street": user_data.get("Street"),
        "House": user_data.get("House"),
        "Flat": user_data.get("Flat"),
        "Gender": Gender.get_label(user_data.get("Gender")),
    }

    await state.set_state(EditInfo.waiting_acception)

    template = render_template("edit_user_info.j2", data=data)

    return await independent_message(template, edit_profile_kb, **kwargs)


# Back button handlers


async def to_main_menu_inline(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.delete()

    return await give_cabinet_menu(state, bot=bot, chat_id=callback.from_user.id)
