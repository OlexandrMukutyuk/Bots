import re

from aiogram import types
from aiogram.filters import BaseFilter


class ValidEmailFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        pattern = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"

        if bool(re.match(pattern, message.text)):
            return True

        return False
