from aiogram import Router

from handlers.advanced.auth import login
from handlers.advanced.auth import register


def prepare_router() -> Router:
    router = Router()

    router.include_router(register.prepare_router())
    router.include_router(login.prepare_router())

    return router
