from handlers.common.reference_info import ReferenceInfoHandlers
from handlers.guest.cabinet.reference_info.handlers import exit_ref_info
from states import ReferenceInfoStates
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.dispatcher.filters.builtin import StateFilter


def prepare_router(dp: Dispatcher):
    dp.text_messages_handler.subscribe(
        exit_ref_info,
        [StateFilter(ReferenceInfoStates.waiting_info), lambda r: r.message.text == "to_menu"],
    )
    dp.text_messages_handler.subscribe(
        ReferenceInfoHandlers.show_info, [StateFilter(ReferenceInfoStates.waiting_info)]
    )
