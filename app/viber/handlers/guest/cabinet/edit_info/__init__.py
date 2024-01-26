from handlers import validation
from handlers.common.helpers import Handler
from handlers.guest.cabinet.edit_info import handlers
from handlers.guest.cabinet.menu import handlers as menu
from keyboards.guest import edit_text
from states import GuestEditInfoStates
from texts import BACK
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.dispatcher.filters.builtin import StateFilter


def prepare_router(dp: Dispatcher):
    message_list = [
        Handler(
            handlers.confirm,
            [
                StateFilter(GuestEditInfoStates.waiting_acceptation),
                lambda r: r.message.text == edit_text["accept_info_text"],
            ],
        ),
        Handler(
            handlers.handle_buttons,
            [
                StateFilter(GuestEditInfoStates.waiting_acceptation),
                lambda r: r.message.text in edit_text.values(),
            ],
        ),
        Handler(menu.change_user_info, [StateFilter(GuestEditInfoStates.waiting_acceptation)]),
        Handler(
            handlers.showing_user_info,
            [StateFilter(GuestEditInfoStates), lambda r: r.message.text == BACK],
        ),
        Handler(
            handlers.handle_buttons,
            [
                StateFilter(GuestEditInfoStates.waiting_acceptation),
                lambda r: r.message.text in edit_text.values(),
            ],
        ),
        # Change street name
        Handler(
            handlers.edit_street,
            [
                StateFilter(GuestEditInfoStates.waiting_street_typing),
                lambda r: len(r.message.text) >= 3,
            ],
        ),
        Handler(
            handlers.confirm_street,
            [
                StateFilter(GuestEditInfoStates.waiting_street_selected),
                lambda r: len(r.message.text) >= 3,
            ],
        ),
        Handler(
            handlers.edit_street,
            [
                StateFilter(GuestEditInfoStates.waiting_street_selected),
                lambda r: len(r.message.text) >= 3,
            ],
        ),
        # Other
        Handler(handlers.edit_house, [StateFilter(GuestEditInfoStates.waiting_house)]),
        Handler(
            validation.not_valid_street_name,
            [StateFilter(GuestEditInfoStates.waiting_street_typing)],
        ),
        Handler(
            validation.not_valid_street_name,
            [StateFilter(GuestEditInfoStates.waiting_street_selected)],
        ),
    ]

    for message in message_list:
        dp.text_messages_handler.subscribe(message.handler, message.filters)
