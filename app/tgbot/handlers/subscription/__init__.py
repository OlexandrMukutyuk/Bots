from aiogram import Router

from handlers.subscription import cabinet
from handlers.subscription.register import handlers


def prepare_router() -> Router:
    router = Router()

    router.include_router(register.prepare_router())
    router.include_router(cabinet.prepare_router())

    return router
