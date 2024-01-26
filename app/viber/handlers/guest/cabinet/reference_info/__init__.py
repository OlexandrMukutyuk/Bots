from handlers.common.reference_info import ReferenceInfoHandlers
from handlers.guest.cabinet.menu.handlers import show_cabinet_menu
from states import ReferenceInfoStates
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.dispatcher.filters.builtin import StateFilter


def prepare_router(dp: Dispatcher):
    dp.text_messages_handler.subscribe(
        show_cabinet_menu,
        [StateFilter(ReferenceInfoStates.waiting_info), lambda r: r.message.text == "to_menu"],
    )
    dp.text_messages_handler.subscribe(
        ReferenceInfoHandlers.show_info, [StateFilter(ReferenceInfoStates.waiting_info)]
    )
