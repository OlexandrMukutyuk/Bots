from aiogram import Router, F

from handlers import validation
from handlers.common.helpers import Handler
from handlers.common.streets import StreetsHandlers
from handlers.guest.auth import handlers
from keyboards.inline.callbacks import StreetCallbackFactory
from states.guest import GuestAuthStates
from texts.keyboards import CHANGE_STREET


def prepare_router() -> Router:
    router = Router()

    message_list = [
        Handler(handlers.type_street, [GuestAuthStates.waiting_street_typing, F.text.len() >= 3]),
        Handler(
            handlers.type_street,
            [GuestAuthStates.waiting_street_selected, ~F.via_bot, F.text.len() >= 3],
        ),
        Handler(
            StreetsHandlers.message_via_bot,
            [GuestAuthStates.waiting_street_selected, F.via_bot],
        ),
        Handler(handlers.change_street, [GuestAuthStates.waiting_house, F.text == CHANGE_STREET]),
        Handler(handlers.save_house, [GuestAuthStates.waiting_house]),
        # Validation
        Handler(validation.not_valid_street_name, [GuestAuthStates.waiting_street_typing]),
        Handler(validation.not_valid_street_name, [GuestAuthStates.waiting_street_selected]),
    ]

    router.inline_query.register(handlers.inline_list, GuestAuthStates.waiting_street_selected)
    router.callback_query.register(
        handlers.confirm_street,
        StreetCallbackFactory.filter(),
        GuestAuthStates.waiting_street_selected,
    )

    for message in message_list:
        router.message.register(message.handler, *message.filters)

    return router
