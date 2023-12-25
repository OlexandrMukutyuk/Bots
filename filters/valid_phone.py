import re

from aiogram import types
from aiogram.filters import BaseFilter


class ValidPhoneFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        pattern = "^\\+{0,1}380\\d{9}$"

        if bool(re.match(pattern, message.text)):
            return True

        return False
