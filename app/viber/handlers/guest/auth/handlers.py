import texts
from dto.guest import RegisterGuestDto
from handlers.common.house import HouseHandlers
from handlers.common.streets import StreetsHandlers
from handlers.guest.cabinet.menu.handlers import show_cabinet_menu
from keyboards.streets import change_street_kb
from services.database import update_last_message
from services.http_client import HttpGuestBot
from states.guest import GuestAuthStates, GuestCabinetStates
from viber import viber
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.types import requests, messages


async def type_street(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    return await StreetsHandlers.choose_street(
        request=request, state=state, new_state=GuestAuthStates.waiting_street_selected
    )


async def confirm_street(request: requests.ViberMessageRequest, data: dict):
    text_list = request.message.text.split(":")

    street_id = int(text_list[1])
    city_id = int(text_list[2])

    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    async def action():
        await state.set_state(GuestAuthStates.waiting_house)

        sender_id = request.sender.id
        await update_last_message(sender_id, texts.ASKING_HOUSE, change_street_kb)

        await viber.send_message(
            sender_id,
            messages.KeyboardMessage(text=texts.ASKING_HOUSE, keyboard=change_street_kb),
        )

    return await StreetsHandlers.confirm_street(
        street_id=street_id, city_id=city_id, state=state, action=action
    )


async def change_street(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    await state.set_state(GuestAuthStates.waiting_street_typing)

    sender_id = request.sender.id
    await update_last_message(sender_id, texts.ASKING_STREET)

    await viber.send_message(
        sender_id,
        messages.TextMessage(text=texts.ASKING_STREET),
    )


async def save_house(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    async def callback():
        state_data = await state.get_data()

        response = await HttpGuestBot.register(
            RegisterGuestDto(street_id=state_data.get("StreetId"), house=state_data.get("House"))
        )

        await state.update_data(GuestId=response.get("GuestId"))

        await show_cabinet_menu(request, state_data)

    await HouseHandlers.change_house(
        request=request,
        state=state,
        new_state=GuestCabinetStates.waiting_menu,
        callback=callback,
    )
