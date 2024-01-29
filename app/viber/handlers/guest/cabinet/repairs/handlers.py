import texts
from dto.guest.repairs_guest import RepairsGuestDto
from handlers.common.streets import StreetsHandlers
from handlers.guest.cabinet.menu.handlers import show_cabinet_menu
from keyboards.common import back_kb
from services.database import update_last_message
from services.http_client import HttpGuestBot
from states import RepairsStates
from utils.template_engine import render_template
from viber import viber
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.types import requests, messages


async def my_address_repairs(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)
    data = await state.get_data()

    repairs = await HttpGuestBot.get_repairs(
        RepairsGuestDto(
            guest_id=data.get("GuestId"), street_id=data.get("StreetId"), house=data.get("House")
        )
    )

    sender_id = request.sender.id

    if len(repairs) == 0:
        await viber.send_message(
            sender_id,
            messages.KeyboardMessage(text=texts.NO_REPAIRS),
        )

    else:
        for repair in repairs:
            template = render_template("show_repair.j2", repair=repair)
            await viber.send_message(
                sender_id,
                messages.TextMessage(text=template),
            )

    await show_cabinet_menu(request, data)


async def other_address_repairs(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    await state.set_state(RepairsStates.waiting_street_typing)

    sender_id = request.sender.id
    await update_last_message(sender_id, texts.ASKING_STREET, back_kb)

    await viber.send_message(
        sender_id,
        messages.KeyboardMessage(text=texts.ASKING_STREET, keyboard=back_kb),
    )


async def type_street(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    return await StreetsHandlers.choose_street(
        request=request, state=state, new_state=RepairsStates.waiting_street_selected
    )


async def confirm_street(request: requests.ViberMessageRequest, data: dict):
    text_list = request.message.text.split(":")

    street_id = int(text_list[1])
    city_id = int(text_list[2])

    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    async def action():
        await state.update_data(RepairStreetId=street_id, Streets=None)
        await state.set_state(RepairsStates.waiting_house)

        sender_id = request.sender.id
        await update_last_message(sender_id, texts.ASKING_HOUSE)

        await viber.send_message(
            sender_id,
            messages.TextMessage(text=texts.ASKING_HOUSE),
        )

    return await StreetsHandlers.confirm_street(
        street_id=street_id, city_id=city_id, state=state, action=action
    )


async def save_house(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)
    data = await state.get_data()

    house = request.message.text
    sender_id = request.sender.id

    repairs = await HttpGuestBot.get_repairs(
        RepairsGuestDto(
            guest_id=data.get("GuestId"), street_id=data.get("RepairStreetId"), house=house
        )
    )

    if len(repairs) == 0:
        await viber.send_message(
            sender_id,
            messages.TextMessage(text=texts.NO_REPAIRS),
        )
    else:
        for repair in repairs:
            await viber.send_message(
                sender_id,
                messages.TextMessage(text=render_template("show_repair.j2", repair=repair)),
            )

    await show_cabinet_menu(request, data)
