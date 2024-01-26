import texts
from dto.guest import GuestIdDto
from handlers.common.enterprises import EnterprisesHandlers
from keyboards.cabinet import guest_menu_kb, guest_menu_text
from services.http_client import HttpGuestBot
from states import GuestCabinetStates, GuestRateEnterpriseStates
from viber import viber
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.types import requests, messages


async def show_cabinet_menu(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    await state.set_state(GuestCabinetStates.waiting_menu)

    await viber.send_message(
        request.sender.id,
        messages.KeyboardMessage(
            text=texts.SUGGEST_HELP, keyboard=guest_menu_kb, min_api_version="3"
        ),
    )


async def main_handler(request: requests.ViberMessageRequest, data: dict):
    button_text = request.message.text

    if button_text == guest_menu_text["review_enterprises"]:
        return await rate_enterprises_list(request, data)


#     if button_text == guest_menu_text["share_chatbot"]:
#         return await share_chatbot(request, data)
#
#     if button_text == guest_menu_text["change_info"]:
#         return await change_user_info(request, data)
#
#     if button_text == guest_menu_text["full_registration"]:
#         return await full_registration(request, data)
#
#     if button_text == guest_menu_text["reference_info"]:
#         return await reference_info(request, data)
#
#     if button_text == guest_menu_text["repairs"]:
#         return await repairs(request, data)


async def rate_enterprises_list(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    async def get_enterprises():
        guest_id = (await state.get_data()).get("GuestId")
        return await HttpGuestBot.get_enterprises(GuestIdDto(guest_id=guest_id))

    async def menu_callback():
        return await show_cabinet_menu(request, data)

    return await EnterprisesHandlers.enterprises_list(
        request=request,
        state=state,
        get_enterprises=get_enterprises,
        new_state=GuestRateEnterpriseStates.showing_list,
        menu_callback=menu_callback,
    )
