import texts
from dto.dto.chat_bot.repairs import RepairsDto
from handlers.common.helpers import full_cabinet_menu
from handlers.common.streets import StreetsHandlers
from keyboards.common import back_kb
from services.http_client import HttpChatBot
from states import FullRepairsStates
from utils.template_engine import render_template
from viber import viber
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.types import requests, messages


async def my_address_repairs(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)
    data = await state.get_data()
    sender_id = request.sender.id
    print(data)

    repairs = await HttpChatBot.get_repairs(
        RepairsDto(
            user_id=data.get("UserId"),
            street_id=data.get("StreetId"),
        )
    )

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

    await full_cabinet_menu(request, data)


async def other_address_repairs(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    await state.set_state(FullRepairsStates.waiting_street_typing)
    await viber.send_message(
        sender_id,
        messages.KeyboardMessage(text=texts.ASKING_STREET, keyboard=back_kb),
    )


async def type_street(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    return await StreetsHandlers.choose_street(
        request=request, state=state, new_state=FullRepairsStates.waiting_street_selected
    )


async def confirm_street(request: requests.ViberMessageRequest, data: dict):
    text_list = request.message.text.split(":")

    street_id = int(text_list[1])
    city_id = int(text_list[2])

    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    async def action():
        await state.update_data(RepairStreetId=street_id, Streets=None)
        await show_repairs(request, data)

    return await StreetsHandlers.confirm_street(
        street_id=street_id, city_id=city_id, state=state, action=action
    )


async def show_repairs(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    data = await state.get_data()
    sender_id = request.sender.id

    repairs = await HttpChatBot.get_repairs(
        RepairsDto(
            user_id=data.get("UserId"),
            street_id=data.get("StreetId"),
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

    await full_cabinet_menu(request, data)
