from handlers.guest.cabinet.menu import handlers
from keyboards.cabinet import guest_menu_text
from states import GuestCabinetStates
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.dispatcher.filters.builtin import StateFilter


def prepare_router(dp: Dispatcher):
    dp.text_messages_handler.subscribe(
        handlers.main_handler,
        [
            StateFilter(GuestCabinetStates.waiting_menu),
            lambda r: r.message.text in guest_menu_text.values(),
        ],
    )

    dp.text_messages_handler.subscribe(
        handlers.show_cabinet_menu, [StateFilter(GuestCabinetStates.waiting_menu)]
    )
