from typing import Callable

from texts.keyboards import WITHOUT_FLAT, LIVING_IN_HOUSE
from viberio.fsm.context import FSMContext
from viberio.fsm.states import State
from viberio.types import requests


class FlatHandlers:
    @staticmethod
    async def change_flat(
        request: requests.ViberMessageRequest, state: FSMContext, new_state: State, callback: Callable
    ):
        flat = request.message.text

        if flat == WITHOUT_FLAT or flat == LIVING_IN_HOUSE:
            flat = None

        await state.update_data(Flat=flat)
        await state.set_state(new_state)

        return await callback()
