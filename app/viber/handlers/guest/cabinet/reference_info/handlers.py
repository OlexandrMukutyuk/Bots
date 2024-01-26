from handlers.common.helpers import update_guest_state_data
from handlers.guest.cabinet.menu.handlers import show_cabinet_menu
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.types import requests


async def exit_ref_info(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    await update_guest_state_data(state)

    await show_cabinet_menu(request, data)
