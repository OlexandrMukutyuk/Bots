from aiogram import types
from aiogram.filters import BaseFilter

from texts.keyboards import BACK


class BackFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        if message.text == BACK:
            return True

        return False
