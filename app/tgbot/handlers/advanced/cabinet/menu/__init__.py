from aiogram import Router, F

from handlers.advanced.cabinet.menu import handlers
from keyboards.default.cabinet.menu import cabinet_menu_text
from states.advanced import FullCabinetStates


def prepare_router() -> Router:
    router = Router()

    router.message.register(
        handlers.main_handler,
        FullCabinetStates.waiting_menu,
        F.text.in_(cabinet_menu_text.values()),
    )

    router.message.register(handlers.show_cabinet_menu, FullCabinetStates.waiting_menu)

    return router
