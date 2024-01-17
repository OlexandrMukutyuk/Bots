from aiogram import Router, F

from handlers.guest.cabinet.menu import handlers
from keyboards.default.guest.auth import guest_menu_text
from states.guest import GuestCabinetStates


def prepare_router() -> Router:
    router = Router()

    router.message.register(
        handlers.main_handler,
        GuestCabinetStates.waiting_menu,
        F.text.in_(guest_menu_text.values()),
    )
    router.message.register(handlers.show_cabinet_menu, GuestCabinetStates.waiting_menu)

    return router
