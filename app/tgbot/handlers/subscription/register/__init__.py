from aiogram import Router, F

from handlers.common.helpers import Handler
from handlers.subscription.register import handlers
from keyboards.inline.callbacks import StreetCallbackFactory
from states.subscription import SubscribeAuthState
from texts.keyboards import CHANGE_STREET


def prepare_router() -> Router:
    router = Router()

    message_list = [
        Handler(handlers.type_street, [SubscribeAuthState.waiting_street_typing]),
        Handler(handlers.type_street, [SubscribeAuthState.waiting_street_selected, ~F.via_bot]),
        Handler(
            handlers.delete_callback_message,
            [SubscribeAuthState.waiting_street_selected, F.via_bot],
        ),
        Handler(
            handlers.change_street, [SubscribeAuthState.waiting_house, F.text == CHANGE_STREET]
        ),
        Handler(handlers.save_house, [SubscribeAuthState.waiting_house]),
    ]

    router.inline_query.register(handlers.inline_list, SubscribeAuthState.waiting_street_selected)
    router.callback_query.register(
        handlers.confirm_street,
        StreetCallbackFactory.filter(),
        SubscribeAuthState.waiting_street_selected,
    )

    for message in message_list:
        router.message.register(message.handler, *message.filters)

    return router
