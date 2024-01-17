import re

from aiogram import types
from aiogram.filters import BaseFilter


class ValidNameFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        pattern = "^[А-Яа-яІіЇї]+[-']{0,2}[А-Яа-яІіЇї]+$"

        if bool(re.match(pattern, message.text)):
            return True

        return False
