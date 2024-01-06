from aiogram import Router

from app.tgbot.handlers.auth.login import handlers
from app.tgbot.states.auth import LoginState


def prepare_router() -> Router:
    router = Router()

    router.message.register(handlers.check_email_code, LoginState.waiting_code)

    return router
