from aiogram import types
from aiogram.filters import BaseFilter

from keyboards.default.start import no_text


class NoFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        if message.text == no_text:
            return True

        return False
