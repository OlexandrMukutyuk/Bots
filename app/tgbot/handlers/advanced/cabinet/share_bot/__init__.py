from aiogram import Router

from handlers.advanced.cabinet import common
from handlers.advanced.cabinet.menu import handlers as menu_handlers
from states.advanced import FullShareChatbotStates


def prepare_router() -> Router:
    router = Router()

    router.message.register(menu_handlers.share_chatbot, FullShareChatbotStates.waiting_back)
    router.callback_query.register(common.back_to_menu, FullShareChatbotStates.waiting_back)

    return router
