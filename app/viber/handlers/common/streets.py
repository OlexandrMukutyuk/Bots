from typing import Callable

import texts
from dto.chat_bot import SearchDto
from keyboards.streets import streets_keyboard
from services.http_client import HttpChatBot, HttpInfoClient
from viber import viber
from viberio.fsm.context import FSMContext
from viberio.fsm.states import State
from viberio.types import requests, messages


class StreetsHandlers:
    @staticmethod
    async def choose_street(
        request: requests.ViberMessageRequest, state: FSMContext, new_state: State
    ):
        streets_data = await HttpChatBot.fetch_streets(SearchDto(search=request.message.text))

        chat_id = request.sender.id
        if len(streets_data) == 0:
            await viber.send_messages(
                chat_id,
                [
                    messages.TextMessage(text=texts.NOT_FOUND),
                    messages.TextMessage(text=texts.ASKING_STREET),
                ],
            )
            return

        await viber.send_message(
            chat_id,
            messages.KeyboardMessage(
                text=texts.PICK_STREET, keyboard=streets_keyboard(streets_data), min_api_version="4"
            ),
        )

        await state.update_data(Streets=streets_data)
        await state.set_state(new_state)

    @staticmethod
    async def confirm_street(
        street_id: int,
        city_id: int,
        state: FSMContext,
        action: Callable,
    ):
        street = await HttpInfoClient.get_street_by_id(street_id)
        city = await HttpInfoClient.get_street_by_id(city_id)

        data = await state.get_data()

        await state.set_data(
            {
                **data,
                "Street": street.get("name"),
                "City": city.get("name"),
                "StreetId": street_id,
                "CityId": city_id,
                "Streets": None,
            }
        )

        await action()