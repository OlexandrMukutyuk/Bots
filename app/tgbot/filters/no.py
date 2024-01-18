from aiogram import types
from aiogram.filters import BaseFilter

from texts import NO


class NoFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        if message.text == NO:
            return True

        return False
