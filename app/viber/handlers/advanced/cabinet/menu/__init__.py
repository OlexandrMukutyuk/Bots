from handlers.advanced.cabinet.menu import handlers
from handlers.common import helpers
from keyboards.cabinet import cabinet_menu_text
from states import FullCabinetStates
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.dispatcher.filters.builtin import StateFilter


def prepare_router(dp: Dispatcher):
    dp.text_messages_handler.subscribe(
        handlers.main_handler,
        [
            StateFilter(FullCabinetStates.waiting_menu),
            lambda r: r.message.text in cabinet_menu_text.values(),
        ],
    )

    dp.text_messages_handler.subscribe(
        helpers.full_cabinet_menu,
        [
            StateFilter(FullCabinetStates.waiting_menu)
        ],
    )

