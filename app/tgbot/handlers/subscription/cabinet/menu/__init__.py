from aiogram import Router, F

from handlers.subscription.cabinet.menu import handlers
from keyboards.default.subscription.subscription import subscription_menu_text
from states.subscription import SubscribeCabinet


def prepare_router() -> Router:
    router = Router()

    router.message.register(
        handlers.main_handler,
        SubscribeCabinet.waiting_menu,
        F.text.in_(subscription_menu_text.values()),
    )
    router.message.register(handlers.show_cabinet_menu, SubscribeCabinet.waiting_menu)

    return router
