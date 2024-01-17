from aiogram import types
from aiogram.filters import BaseFilter


class ValidFlatFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        min = 1
        max = 99

        flat_value = message.text

        if flat_value.isdigit() and min <= int(flat_value) <= max:
            return True

        return False
