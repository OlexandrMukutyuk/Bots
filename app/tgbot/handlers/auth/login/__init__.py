from aiogram import Router

from handlers.auth.login import handlers
from states.auth import LoginState


def prepare_router() -> Router:
    router = Router()

    router.message.register(handlers.check_email_code, LoginState.waiting_code)

    return router
