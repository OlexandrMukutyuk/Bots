from aiogram import Router

from app.tgbot.handlers.cabinet import handlers
from app.tgbot.handlers.cabinet.menu import handlers as menu_handlers
from app.tgbot.states.cabinet import ShareChatbot


def prepare_router() -> Router:
    router = Router()

    router.message.register(menu_handlers.share_chatbot, ShareChatbot.waiting_back)
    router.callback_query.register(handlers.back_to_menu, ShareChatbot.waiting_back)

    return router
