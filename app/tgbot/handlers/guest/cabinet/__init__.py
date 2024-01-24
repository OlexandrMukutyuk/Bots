from aiogram import Router

from handlers.guest.cabinet import rate_enterprises, share_bot, full_register, edit_info, reference_info, repairs
from handlers.guest.cabinet.menu import handlers


def prepare_router() -> Router:
    router = Router()

    router.include_router(menu.prepare_router())
    router.include_router(rate_enterprises.prepare_router())
    router.include_router(share_bot.prepare_router())
    router.include_router(edit_info.prepare_router())
    router.include_router(reference_info.prepare_router())
    router.include_router(repairs.prepare_router())
    router.include_router(full_register.prepare_router())

    return router
