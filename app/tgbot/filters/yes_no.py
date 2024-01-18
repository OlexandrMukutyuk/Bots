from aiogram import types
from aiogram.filters import BaseFilter

from texts import NO, YES


class YesNoFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        if message.text in [YES, NO]:
            return True

        return False
