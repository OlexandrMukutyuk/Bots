from aiogram import types
from aiogram.filters import BaseFilter

from keyboards.default.start import yes_text


class YesFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        if message.text == yes_text:
            return True

        return False
