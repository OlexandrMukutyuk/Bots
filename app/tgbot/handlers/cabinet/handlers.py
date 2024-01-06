from aiogram import types, Bot
from aiogram.fsm.context import FSMContext

from app.tgbot.handlers.cabinet.menu.handlers import give_cabinet_menu
from app.tgbot.states.cabinet import CabinetStates


async def back_to_menu(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(CabinetStates.waiting_menu)

    await give_cabinet_menu(state=state, bot=bot, chat_id=callback.from_user.id)

    if callback.message:
        await callback.message.delete()

    await callback.answer()
