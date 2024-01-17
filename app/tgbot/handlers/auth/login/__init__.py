from aiogram import Router
from states.advanced import LoginState

from handlers.auth.login import handlers


def prepare_router() -> Router:
    router = Router()

    router.message.register(handlers.check_email_code, LoginState.waiting_code)

    return router
