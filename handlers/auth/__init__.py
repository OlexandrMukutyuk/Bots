from aiogram import Router

from ..auth import register


def prepare_router() -> Router:
    router = Router()

    router.include_router(register.prepare_router())

    return router
