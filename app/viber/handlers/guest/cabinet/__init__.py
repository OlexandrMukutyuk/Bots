from handlers.guest.cabinet import menu, rate_enterprises, reference_info
from viberio.dispatcher.dispatcher import Dispatcher


def prepare_router(dp: Dispatcher):
    menu.prepare_router(dp)
    rate_enterprises.prepare_router(dp)
    reference_info.prepare_router(dp)
