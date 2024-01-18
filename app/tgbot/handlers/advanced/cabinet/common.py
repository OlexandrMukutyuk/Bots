from aiogram import types, Bot
from aiogram.fsm.context import FSMContext

from handlers.common.helpers import full_cabinet_menu
from states.advanced import FullCabinetStates


async def back_to_menu(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(FullCabinetStates.waiting_menu)

    await full_cabinet_menu(state=state, bot=bot, chat_id=callback.from_user.id)

    if callback.message:
        await callback.message.delete()

    await callback.answer()
