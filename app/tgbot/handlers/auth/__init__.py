from aiogram import Router

from handlers.auth import login
from handlers.auth import register


def prepare_router() -> Router:
    router = Router()

    router.include_router(register.prepare_router())
    router.include_router(login.prepare_router())

    return router
