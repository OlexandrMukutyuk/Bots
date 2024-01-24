from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.common.helpers import update_guest_state_data
from handlers.guest.cabinet.menu.handlers import to_main_menu_inline


async def exit_ref_info(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await update_guest_state_data(state)

    await to_main_menu_inline(callback, state, bot)
