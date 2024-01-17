from aiogram import Router, F
from aiogram.filters import StateFilter

from handlers import validation
from handlers.common.helpers import Handler
from handlers.guest.cabinet.edit_info import handlers
from handlers.guest.cabinet.menu import handlers as menu
from keyboards.default.guest.edit_info import edit_text
from keyboards.inline.callbacks import StreetCallbackFactory
from states import GuestEditInfoStates
from texts import BACK


def prepare_router() -> Router:
    router = Router()

    message_list = [
        Handler(
            handlers.confirm,
            [GuestEditInfoStates.waiting_acceptation, F.text == edit_text["accept_info_text"]],
        ),
        Handler(
            handlers.handle_buttons,
            [GuestEditInfoStates.waiting_acceptation, F.text.in_(edit_text.values())],
        ),
        Handler(menu.change_user_info, [GuestEditInfoStates.waiting_acceptation]),
        Handler(handlers.showing_user_info, [StateFilter(GuestEditInfoStates), F.text == BACK]),
        Handler(
            handlers.handle_buttons,
            [GuestEditInfoStates.waiting_acceptation, F.text.in_(edit_text.values())],
        ),
        # Change street name
        Handler(
            handlers.edit_street, [GuestEditInfoStates.waiting_street_typing, F.text.len() >= 3]
        ),
        Handler(
            handlers.edit_street,
            [GuestEditInfoStates.waiting_street_selected, ~F.via_bot, F.text.len() >= 3],
        ),
        Handler(handlers.message_via_bot, [GuestEditInfoStates.waiting_street_selected, F.via_bot]),
        # Other
        Handler(handlers.edit_house, [GuestEditInfoStates.waiting_house]),
        Handler(validation.not_valid_street_name, [GuestEditInfoStates.waiting_street_typing]),
        Handler(validation.not_valid_street_name, [GuestEditInfoStates.waiting_street_selected]),
    ]

    router.inline_query.register(
        handlers.show_street_list, GuestEditInfoStates.waiting_street_selected
    )
    router.callback_query.register(
        handlers.confirm_street,
        StreetCallbackFactory.filter(),
        GuestEditInfoStates.waiting_street_selected,
    )

    for message in message_list:
        router.message.register(message.handler, *message.filters)

    return router
