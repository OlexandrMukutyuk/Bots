from handlers.advanced import auth, cabinet
from viberio.dispatcher.dispatcher import Dispatcher


def prepare_router(dp: Dispatcher):
    auth.prepare_router(dp)
    cabinet.prepare_router(dp)
