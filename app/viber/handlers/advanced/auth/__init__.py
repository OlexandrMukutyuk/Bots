from handlers.advanced.auth import login, register
from viberio.dispatcher.dispatcher import Dispatcher


def prepare_router(dp: Dispatcher):
    login.prepare_router(dp)
    register.prepare_router(dp)
