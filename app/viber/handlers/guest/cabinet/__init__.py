from handlers.guest.cabinet import menu, rate_enterprises
from viberio.dispatcher.dispatcher import Dispatcher


def prepare_router(dp: Dispatcher):
    menu.prepare_router(dp)
    rate_enterprises.prepare_router(dp)
