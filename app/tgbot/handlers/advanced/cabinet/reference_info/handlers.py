from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.advanced.cabinet.menu.handlers import to_main_menu_inline
from handlers.common.helpers import update_user_state_data


async def exit_ref_info(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await update_user_state_data(state)

    await to_main_menu_inline(callback, state, bot)
