import re

from aiogram import types
from aiogram.filters import BaseFilter


class StrongPasswordFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        s = message.text

        latin_alphanumeric_pattern = "^[A-Za-z0-9~!@#$%^&*()_+]+$"

        if len(s) < 6:
            return False
        if not re.search("[a-z]", s):
            return False
        if not re.search("[A-Z]", s):
            return False
        if not re.search("[0-9]", s):
            return False
        if not re.search("[~!@#$%^&*()_+]", s):
            return False
        if not re.match(latin_alphanumeric_pattern, s):
            return False

        return True
