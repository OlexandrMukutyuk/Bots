from aiogram import Router

from . import start, login
from ..auth import register


def prepare_router() -> Router:
    router = Router()

    router.include_router(start.prepare_router())
    router.include_router(register.prepare_router())
    router.include_router(login.prepare_router())

    return router
