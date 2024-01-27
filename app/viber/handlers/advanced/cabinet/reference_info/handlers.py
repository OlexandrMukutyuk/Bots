from handlers.common.helpers import update_user_state_data, full_cabinet_menu
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.types import requests


async def exit_ref_info(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    await update_user_state_data(state)

    await full_cabinet_menu(request, data)
