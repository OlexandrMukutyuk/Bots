from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

import texts
from dto.guest import RegisterGuestDto
from handlers.common.house import HouseHandlers
from handlers.common.streets import StreetsHandlers
from handlers.subscription.cabinet.menu.handlers import show_cabinet_menu
from keyboards.default.common import change_street_kb
from keyboards.inline.callbacks import StreetCallbackFactory
from services.http_client import HttpGuestBot
from states.subscription import AuthStates, SubscribeCabinet


async def type_street(message: types.Message, state: FSMContext, bot: Bot):
    return await StreetsHandlers.choose_street(
        message=message, state=state, new_state=AuthStates.waiting_street_selected, bot=bot
    )


async def delete_callback_message(message: types.Message, state: FSMContext, bot: Bot):
    return await StreetsHandlers.message_via_bot(message, state, bot)


async def inline_list(callback: types.InlineQuery, state: FSMContext):
    streets: list = (await state.get_data()).get("Streets")

    return await StreetsHandlers.inline_list(callback, streets)


async def confirm_street(
    callback: types.CallbackQuery, callback_data: StreetCallbackFactory, state: FSMContext, bot: Bot
):
    async def action():
        await state.set_state(AuthStates.waiting_house)
        await bot.send_message(
            chat_id=callback.from_user.id, text=texts.ASKING_HOUSE, reply_markup=change_street_kb
        )

    return await StreetsHandlers.confirm_street(
        callback=callback, callback_data=callback_data, state=state, action=action, bot=bot
    )


async def change_street(message: types.Message, state: FSMContext):
    await state.set_state(AuthStates.waiting_street_typing)
    await message.answer(text=texts.ASKING_STREET, reply_markup=ReplyKeyboardRemove())


async def save_house(message: types.Message, state: FSMContext):
    async def callback():
        data = await state.get_data()

        response = await HttpGuestBot.register(
            RegisterGuestDto(street_id=data.get("StreetId"), house=data.get("House"))
        )

        await state.update_data(GuestId=response.get("GuestId"))

        await show_cabinet_menu(message, state)

    await HouseHandlers.change_house(
        message=message,
        state=state,
        new_state=SubscribeCabinet.waiting_menu,
        callback=callback,
    )
