from asyncio import sleep

import texts
from dto.guest import GuestIdDto
from handlers.common.enterprises import EnterprisesHandlers
from handlers.common.reference_info import ReferenceInfoHandlers
from keyboards.cabinet import guest_menu_kb, guest_menu_text
from keyboards.guest import edit_guest_kb, full_registration_kb
from keyboards.repairs import repairs_kb
from services.database import update_last_message
from services.http_client import HttpGuestBot
from states import (
    GuestCabinetStates,
    GuestRateEnterpriseStates,
    ReferenceInfoStates,
    GuestEditInfoStates,
    RepairsStates,
    GuestFullRegisterStates,
)
from utils.template_engine import render_template
from viber import viber
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.types import requests, messages


async def show_cabinet_menu(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    await state.set_state(GuestCabinetStates.waiting_menu)

    sender_id = request.sender.id
    await update_last_message(sender_id, texts.SUGGEST_HELP, guest_menu_kb)

    await sleep(0.2)

    await viber.send_message(
        sender_id,
        messages.KeyboardMessage(
            text=texts.SUGGEST_HELP, keyboard=guest_menu_kb, min_api_version="3"
        ),
    )


async def main_handler(request: requests.ViberMessageRequest, data: dict):
    button_text = request.message.text

    if button_text == guest_menu_text["review_enterprises"]:
        return await rate_enterprises_list(request, data)
    if button_text == guest_menu_text["reference_info"]:
        return await reference_info(request, data)

    if button_text == guest_menu_text["change_info"]:
        return await change_user_info(request, data)

    if button_text == guest_menu_text["repairs"]:
        return await repairs(request, data)

    if button_text == guest_menu_text["full_registration"]:
        return await full_registration(request, data)


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


async def reference_info(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    await ReferenceInfoHandlers.load_menu(
        request=request, state=state, parent_id=None, new_state=ReferenceInfoStates.waiting_info
    )


async def change_user_info(request: requests.ViberMessageRequest, data: dict):
    await send_edit_guest_info(request, data)


async def send_edit_guest_info(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    user_data = await state.get_data()

    data = {
        "Street": user_data.get("Street"),
        "House": user_data.get("House"),
    }

    template = render_template("edit_guest_info.j2", data=data)

    await state.set_state(GuestEditInfoStates.waiting_acceptation)

    sender_id = request.sender.id
    await update_last_message(sender_id, template, edit_guest_kb)


    return await viber.send_message(
        sender_id,
        messages.KeyboardMessage(text=template, keyboard=edit_guest_kb, min_api_version="3"),
    )


async def repairs(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    sender_id = request.sender.id
    await update_last_message(sender_id, texts.ASKING_REPAIRS, repairs_kb)

    await viber.send_messages(
        sender_id,
        [
            messages.KeyboardMessage(
                text=texts.ASKING_REPAIRS, keyboard=repairs_kb, min_api_version="3"
            ),
        ],
    )

    return await state.set_state(RepairsStates.waiting_address)


async def full_registration(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    await state.set_state(GuestFullRegisterStates.waiting_answer)

    sender_id = request.sender.id
    await update_last_message(sender_id, texts.FULL_REGISTER_INFO, full_registration_kb)

    return await viber.send_message(
        sender_id,
        messages.KeyboardMessage(
            text=texts.FULL_REGISTER_INFO, keyboard=full_registration_kb, min_api_version="3"
        ),
    )
