from aiogram import Router

from handlers.advanced import auth, cabinet


def prepare_router() -> Router:
    router = Router()

    router.include_router(auth.prepare_router())
    router.include_router(cabinet.prepare_router())

    return router
