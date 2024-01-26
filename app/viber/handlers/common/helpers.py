from typing import NamedTuple, Callable

from dto.chat_bot import UserIdDto
from services.http_client import HttpChatBot
from viberio.fsm.context import FSMContext


class Handler(NamedTuple):
    handler: Callable
    filters: list


async def update_user_state_data(state: FSMContext):
    data = await state.get_data()

    id = data.get("UserId")

    user_params = await HttpChatBot.get_user_params(UserIdDto(user_id=id))

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
