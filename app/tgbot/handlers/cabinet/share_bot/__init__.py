from aiogram import Router

from handlers.cabinet import common
from handlers.cabinet.menu import handlers as menu_handlers
from states.cabinet import ShareChatbot


def prepare_router() -> Router:
    router = Router()

    router.message.register(menu_handlers.share_chatbot, ShareChatbot.waiting_back)
    router.callback_query.register(common.back_to_menu, ShareChatbot.waiting_back)

    return router
