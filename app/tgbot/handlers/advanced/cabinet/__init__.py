from aiogram import Router

from handlers.advanced.cabinet import archive_req, rate_enterprises, menu, reference_info, repairs
from handlers.advanced.cabinet import create_request, share_bot, issue_report, edit_profile


def prepare_router() -> Router:
    router = Router()

    router.include_router(menu.prepare_router())
    router.include_router(create_request.prepare_router())
    router.include_router(share_bot.prepare_router())
    router.include_router(issue_report.prepare_router())
    router.include_router(rate_enterprises.prepare_router())
    router.include_router(archive_req.prepare_router())
    router.include_router(edit_profile.prepare_router())
    router.include_router(repairs.prepare_router())
    router.include_router(reference_info.prepare_router())

    return router
