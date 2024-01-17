from aiogram import Router, F

from handlers.common.helpers import Handler
from handlers.subscription.cabinet import handlers
from keyboards.default.subscription.subscription import subscription_menu_text
from states.subscription import SubscribeCabinet, SubscribeShareBot, SubscribeRateEnterprise


def prepare_router() -> Router:
    router = Router()

    message_list = [
        # Menu
        Handler(
            handlers.main_handler,
            [SubscribeCabinet.waiting_menu, F.text.in_(subscription_menu_text.values())],
        ),
        Handler(handlers.show_cabinet_menu, [SubscribeCabinet.waiting_menu]),
    ]

    callback_list = [
        Handler(handlers.to_main_menu_inline, [SubscribeShareBot.waiting_back]),
        Handler(
            handlers.to_main_menu_inline, [SubscribeRateEnterprise.showing_list, F.data == "back"]
        ),
    ]

    for message in message_list:
        router.message.register(message.handler, *message.filters)

    for callback in callback_list:
        router.callback_query.register(callback.handler, *callback.filters)

    return router
