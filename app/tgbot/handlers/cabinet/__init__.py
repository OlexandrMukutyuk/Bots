from aiogram import Router

from app.tgbot.handlers.cabinet import create_request, share_bot, issue_report, rate_enterprises, archive_req, \
    edit_profile
from app.tgbot.handlers.cabinet.menu import handlers


def prepare_router() -> Router:
    router = Router()

    router.include_router(menu.prepare_router())
    router.include_router(create_request.prepare_router())
    router.include_router(share_bot.prepare_router())
    router.include_router(issue_report.prepare_router())
    router.include_router(rate_enterprises.prepare_router())
    router.include_router(archive_req.prepare_router())
    router.include_router(edit_profile.prepare_router())

    return router
