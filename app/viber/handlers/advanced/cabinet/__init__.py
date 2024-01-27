from handlers.advanced.cabinet import menu, rate_enterprises, edit_info
from viberio.dispatcher.dispatcher import Dispatcher


def prepare_router(dp: Dispatcher):
    menu.prepare_router(dp)
    rate_enterprises.prepare_router(dp)
    edit_info.prepare_router(dp)
