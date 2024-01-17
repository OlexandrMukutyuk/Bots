from aiogram import Router

from handlers.subscription.cabinet.menu import handlers
from states.subscription import SubscribeShareBot


def prepare_router() -> Router:
    router = Router()

    router.message.register(handlers.share_chatbot, SubscribeShareBot.waiting_back)
    router.callback_query.register(handlers.to_main_menu_inline, SubscribeShareBot.waiting_back)

    return router
