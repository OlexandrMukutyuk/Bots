from aiogram import types
from aiogram.filters import BaseFilter

from keyboards.default.start import yes_text, no_text


class YesNoFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        if message.text in [yes_text, no_text]:
            return True

        return False
