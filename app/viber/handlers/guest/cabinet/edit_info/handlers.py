import texts
from dto.guest import UpdateGuestDto
from handlers.common.house import HouseHandlers
from handlers.common.streets import StreetsHandlers
from handlers.guest.cabinet.menu.handlers import send_edit_guest_info, show_cabinet_menu
from keyboards.common import back_kb
from keyboards.guest import edit_text
from services.http_client import HttpGuestBot
from states import GuestEditInfoStates
from viber import viber
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.types import requests, messages


async def handle_buttons(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    button_type = request.message.text
    sender_id = request.sender.id

    if button_type == edit_text["street_text"]:
        await state.set_state(GuestEditInfoStates.waiting_street_typing)
        await viber.send_message(
            sender_id, messages.KeyboardMessage(text=texts.ASKING_STREET, keyboard=back_kb)
        )
        return

    if button_type == edit_text["house_text"]:
        await state.set_state(GuestEditInfoStates.waiting_house)
        await viber.send_message(
            sender_id, messages.KeyboardMessage(text=texts.ASKING_HOUSE, keyboard=back_kb)
        )
        return


async def showing_user_info(request: requests.ViberMessageRequest, data: dict):
    await send_edit_guest_info(request, data)


async def edit_street(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    return await StreetsHandlers.choose_street(
        request=request, state=state, new_state=GuestEditInfoStates.waiting_street_selected
    )


async def confirm_street(request: requests.ViberMessageRequest, data: dict):
    text_list = request.message.text.split(":")

    street_id = int(text_list[1])
    city_id = int(text_list[2])

    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    async def action():
        await state.set_state(GuestEditInfoStates.waiting_acceptation)
        await send_edit_guest_info(request, data)

    return await StreetsHandlers.confirm_street(
        street_id=street_id, city_id=city_id, state=state, action=action
    )


async def edit_house(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    async def callback():
        await send_edit_guest_info(request, data)

    return await HouseHandlers.change_house(
        request=request,
        state=state,
        new_state=GuestEditInfoStates.waiting_acceptation,
        callback=callback,
    )


async def confirm(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)
    data = await state.get_data()

    await HttpGuestBot.update_data(
        UpdateGuestDto(
            guest_id=data.get("GuestId"),
            street_id=data.get("StreetId"),
            house=data.get("House"),
        )
    )

    await viber.send_message(
        request.sender.id, messages.TextMessage(text=texts.EDITED_SUCCESSFULLY)
    )

    return await show_cabinet_menu(request, data)
