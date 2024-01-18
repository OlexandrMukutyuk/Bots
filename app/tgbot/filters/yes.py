from aiogram import types
from aiogram.filters import BaseFilter

from keyboards.default.start import YES


class YesFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        if message.text == YES:
            return True

        return False
