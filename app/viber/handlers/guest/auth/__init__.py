from handlers import validation
from handlers.common.helpers import Handler
from handlers.guest.auth import handlers
from states import GuestAuthStates
from texts import CHANGE_STREET
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.dispatcher.filters.builtin import StateFilter


def prepare_router(dp: Dispatcher):
    message_list = [
        Handler(
            handlers.type_street,
            [
                StateFilter(GuestAuthStates.waiting_street_typing),
                lambda r: len(r.message.text) >= 3,
            ],
        ),
        Handler(handlers.confirm_street, [StateFilter(GuestAuthStates.waiting_street_selected)]),
        Handler(
            handlers.change_street,
            [StateFilter(GuestAuthStates.waiting_house), lambda r: r.message.text == CHANGE_STREET],
        ),
        Handler(handlers.save_house, [StateFilter(GuestAuthStates.waiting_house)]),
        # # Validation
        Handler(
            validation.not_valid_street_name, [StateFilter(GuestAuthStates.waiting_street_typing)]
        ),
    ]

    for message in message_list:
        dp.text_messages_handler.subscribe(message.handler, message.filters)
