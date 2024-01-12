from aiogram import types
from aiogram.filters import BaseFilter

from keyboards.default.cabinet.create_request import back_text


class BackFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        if message.text == back_text:
            return True

        return False
