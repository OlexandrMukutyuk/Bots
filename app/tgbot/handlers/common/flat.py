from typing import Callable

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from texts.keyboards import WITHOUT_FLAT


class FlatHandlers:
    @staticmethod
    async def change_flat(
        message: types.Message, state: FSMContext, new_state: State, callback: Callable
    ):
        flat = message.text

        if flat == WITHOUT_FLAT:
            flat = None

        await state.update_data(Flat=flat)
        await state.set_state(new_state)

        return await callback()
