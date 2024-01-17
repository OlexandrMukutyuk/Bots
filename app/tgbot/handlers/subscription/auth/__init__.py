from aiogram import Router, F

from handlers import validation
from handlers.common.helpers import Handler
from handlers.subscription.auth import handlers
from keyboards.inline.callbacks import StreetCallbackFactory
from states.subscription import AuthStates
from texts.keyboards import CHANGE_STREET


def prepare_router() -> Router:
    router = Router()

    message_list = [
        Handler(handlers.type_street, [AuthStates.waiting_street_typing, F.text.len() >= 3]),
        Handler(handlers.type_street, [AuthStates.waiting_street_selected, ~F.via_bot]),
        Handler(
            handlers.delete_callback_message,
            [AuthStates.waiting_street_selected, F.via_bot],
        ),
        Handler(handlers.change_street, [AuthStates.waiting_house, F.text == CHANGE_STREET]),
        Handler(handlers.save_house, [AuthStates.waiting_house]),
        # Validation
        Handler(validation.not_valid_street_name, [AuthStates.waiting_street_typing]),
    ]

    router.inline_query.register(handlers.inline_list, AuthStates.waiting_street_selected)
    router.callback_query.register(
        handlers.confirm_street,
        StreetCallbackFactory.filter(),
        AuthStates.waiting_street_selected,
    )

    for message in message_list:
        router.message.register(message.handler, *message.filters)

    return router
