import re

from aiogram import types
from aiogram.filters import BaseFilter


class ValidNameFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        pattern = "^[A-Za-zА-Яа-яІіЇї]+[-']{0,2}[A-Za-zА-Яа-яІіЇї]+$"

        if bool(re.match(pattern, message.text)):
            return True

        return False
