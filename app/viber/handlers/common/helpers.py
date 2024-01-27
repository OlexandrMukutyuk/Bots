from asyncio import sleep
from typing import NamedTuple, Callable

import texts
from dto.chat_bot import UserIdDto
from keyboards.cabinet import cabinet_menu_kb
from services.http_client import HttpChatBot
from states import FullCabinetStates
from viber import viber
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.fsm.context import FSMContext
from viberio.types import requests, messages


class Handler(NamedTuple):
    handler: Callable
    filters: list


async def update_user_state_data(state: FSMContext):
    data = await state.get_data()

    id = data.get("UserId")

    user_params = await HttpChatBot.get_user_params(UserIdDto(user_id=id))

    for key in user_params:
        if user_params[key] in ["", "0"]:
            user_params[key] = None


    await state.set_data({"UserId": id, **user_params})


async def update_guest_state_data(state: FSMContext):
    data = await state.get_data()

    await state.set_data(
        {
            "Street": data.get("Street"),
            "City": data.get("City"),
            "StreetId": data.get("StreetId"),
            "CityId": data.get("CityId"),
            "House": data.get("House"),
            "GuestId": data.get("GuestId"),
        }
    )


async def full_cabinet_menu(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    await state.set_state(FullCabinetStates.waiting_menu)

    await sleep(0.2)

    await viber.send_message(
        request.sender.id,
        messages.KeyboardMessage(
            text=texts.SUGGEST_HELP, keyboard=cabinet_menu_kb, min_api_version="3"
        ),
    )
