from typing import Callable

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

import texts
from dto.chat_bot import VerifyAddressDto
from services.http_client import HttpChatBot


class HouseHandlers:
    @staticmethod
    async def change_house(
        message: types.Message, state: FSMContext, new_state: State, callback: Callable
    ):
        house = message.text

        street_id = (await state.get_data()).get("StreetId")

        is_address_correct = await HttpChatBot.verify_address(
            VerifyAddressDto(street_id=street_id, house=house)
        )

        if not is_address_correct:
            await message.answer(texts.HOUSE_NOT_FOUND)
            await message.answer(texts.ASKING_HOUSE)
            return

        await state.update_data(House=house)
        await state.set_state(new_state)

        await callback()
