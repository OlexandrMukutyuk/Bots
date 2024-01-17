from aiogram import Router

from handlers.guest.cabinet.menu import handlers
from states.guest import GuestShareBotStates


def prepare_router() -> Router:
    router = Router()

    router.message.register(handlers.share_chatbot, GuestShareBotStates.waiting_back)
    router.callback_query.register(handlers.to_main_menu_inline, GuestShareBotStates.waiting_back)

    return router
