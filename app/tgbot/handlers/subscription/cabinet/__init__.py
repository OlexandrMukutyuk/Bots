from aiogram import Router

from handlers.subscription.cabinet import rate_enterprises, share_bot
from handlers.subscription.cabinet.menu import handlers


def prepare_router() -> Router:
    router = Router()

    router.include_router(menu.prepare_router())
    router.include_router(rate_enterprises.prepare_router())
    router.include_router(share_bot.prepare_router())

    return router
