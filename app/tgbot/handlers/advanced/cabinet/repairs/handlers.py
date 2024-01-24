from aiogram import types, Bot
from aiogram.fsm.context import FSMContext

import texts
from dto.chat_bot.repairs import RepairsDto
from handlers.advanced.cabinet.common import back_to_menu
from handlers.common.streets import StreetsHandlers
from keyboards.default.common import back_kb
from keyboards.inline.callbacks import StreetCallbackFactory
from services.http_client import HttpChatBot
from states import FullRepairsStates
from utils.template_engine import render_template


async def my_address_repairs(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()

    repairs = await HttpChatBot.get_repairs(RepairsDto(
        user_id=data.get('UserId'),
        street_id=data.get('StreetId'),
    ))

    if len(repairs) == 0:
        await bot.send_message(text=texts.NO_REPAIRS, chat_id=callback.from_user.id)
    else:
        for repair in repairs:
            template = render_template('show_repair.j2', repair=repair)
            await bot.send_message(text=template, chat_id=callback.from_user.id)

    await back_to_menu(callback, state, bot=bot)

    await callback.answer()


async def other_address_repairs(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    chat_id = callback.message.chat.id

    await callback.message.delete()

    await state.set_state(FullRepairsStates.waiting_street_typing)
    await bot.send_message(text=texts.ASKING_STREET, reply_markup=back_kb, chat_id=chat_id)

    await callback.answer()


async def type_street(message: types.Message, state: FSMContext, bot: Bot):
    return await StreetsHandlers.choose_street(
        message=message, state=state, new_state=FullRepairsStates.waiting_street_selected, bot=bot
    )


async def show_inline_list(callback: types.InlineQuery, state: FSMContext):
    data = (await state.get_data()).get('Streets')
    return await StreetsHandlers.inline_list(callback, streets_data=data)


async def message_via_bot(message: types.Message, state: FSMContext, bot: Bot):
    return await StreetsHandlers.message_via_bot(message, state, bot)


async def confirm_street(
        callback: types.CallbackQuery,
        callback_data: StreetCallbackFactory,
        state: FSMContext,
        bot: Bot,
):
    street_id = callback_data.street_id
    chat_id = callback.from_user.id

    await StreetsHandlers.delete_message(
        chat_id=chat_id, state=state, bot=bot, key=StreetsHandlers.ConfirmCallback
    )

    await state.update_data(RepairStreetId=street_id, Streets=None)
    await state.set_state(FullRepairsStates.waiting_house)

    await show_repairs(callback, state, bot)
    await bot.send_message(text=texts.ASKING_HOUSE, chat_id=chat_id)

    return await callback.answer()


async def show_repairs(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    chat_id = callback.from_user.id

    repairs = await HttpChatBot.get_repairs(RepairsDto(
        user_id=data.get('UserId'),
        street_id=data.get('StreetId'),
    ))

    if len(repairs) == 0:
        await bot.send_message(chat_id=chat_id, text=texts.NO_REPAIRS)
    else:
        for repair in repairs:
            await bot.send_message(chat_id=chat_id, text=render_template('show_repair.j2', repair=repair))

    await back_to_menu(callback, state, bot)
