from aiogram import types, Bot
from aiogram.fsm.context import FSMContext

import texts
from dto.guest import UpdateGuestDto
from handlers.common.house import HouseHandlers
from handlers.common.streets import StreetsHandlers
from handlers.guest.cabinet.menu.handlers import send_edit_guest_info, give_cabinet_menu
from keyboards.default.common import back_kb
from keyboards.default.guest.edit_info import edit_text
from keyboards.inline.callbacks import StreetCallbackFactory
from services.http_client import HttpGuestBot
from states import GuestEditInfoStates


async def handle_buttons(message: types.Message, state: FSMContext):
    button_type = message.text

    if button_type == edit_text["street_text"]:
        await state.set_state(GuestEditInfoStates.waiting_street_typing)
        await message.answer(text=texts.ASKING_STREET, reply_markup=back_kb)
        return

    if button_type == edit_text["house_text"]:
        await state.set_state(GuestEditInfoStates.waiting_house)
        await message.answer(text=texts.ASKING_HOUSE, reply_markup=back_kb)
        return


async def showing_user_info(message: types.Message, state: FSMContext):
    await send_edit_guest_info(state, message=message)


async def edit_street(message: types.Message, state: FSMContext, bot: Bot):
    return await StreetsHandlers.choose_street(
        message=message, state=state, new_state=GuestEditInfoStates.waiting_street_selected, bot=bot
    )


async def message_via_bot(message: types.Message, state: FSMContext, bot: Bot):
    return await StreetsHandlers.message_via_bot(message, state, bot)


async def show_street_list(callback: types.InlineQuery, state: FSMContext):
    data = (await state.get_data()).get("Streets")

    return await StreetsHandlers.inline_list(callback, data)


async def confirm_street(
    callback: types.CallbackQuery, callback_data: StreetCallbackFactory, state: FSMContext, bot: Bot
):
    async def action():
        await state.set_state(GuestEditInfoStates.waiting_acceptation)
        await send_edit_guest_info(state, bot=bot, chat_id=callback.from_user.id)

    await StreetsHandlers.confirm_street(
        callback=callback, callback_data=callback_data, state=state, action=action, bot=bot
    )


async def edit_house(message: types.Message, state: FSMContext):
    async def callback():
        await send_edit_guest_info(state, message=message)

    return await HouseHandlers.change_house(
        message=message,
        state=state,
        new_state=GuestEditInfoStates.waiting_acceptation,
        callback=callback,
    )


async def confirm(message: types.Message, state: FSMContext):
    data = await state.get_data()

    print("Hello")
    await HttpGuestBot.update_data(
        UpdateGuestDto(
            guest_id=data.get("GuestId"),
            street_id=data.get("StreetId"),
            house=data.get("House"),
        )
    )

    await message.answer(texts.EDITED_SUCCESSFULLY)

    return await give_cabinet_menu(state, message=message)
