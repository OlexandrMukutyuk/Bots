from typing import Callable

import texts
from dto.chat_bot import VerifyAddressDto
from services.http_client import HttpChatBot
from viber import viber
from viberio.fsm.context import FSMContext
from viberio.fsm.states import State
from viberio.types import requests, messages


class HouseHandlers:
    @staticmethod
    async def change_house(
        request: requests.ViberMessageRequest,
        state: FSMContext,
        new_state: State,
        callback: Callable,
    ):
        house = request.message.text

        street_id = (await state.get_data()).get("StreetId")

        is_address_correct = await HttpChatBot.verify_address(
            VerifyAddressDto(street_id=street_id, house=house)
        )

        if not is_address_correct:
            await viber.send_messages(
                request.sender.id,
                [
                    messages.TextMessage(text=texts.HOUSE_NOT_FOUND),
                    messages.TextMessage(text=texts.ASKING_HOUSE),
                ],
            )
            return

        await state.update_data(House=house)
        await state.set_state(new_state)

        await callback()
