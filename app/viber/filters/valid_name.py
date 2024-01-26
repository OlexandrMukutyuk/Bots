import re

from viberio.dispatcher.filters.filters import Filter
from viberio.types.requests import ViberMessageRequest


class ValidNameFilter(Filter):
    async def check(self, event):
        if isinstance(event, ViberMessageRequest):
            pattern = "^[А-Яа-яІіЇї]+[-']{0,2}[А-Яа-яІіЇї]+$"

            if bool(re.match(pattern, event.message.text)):
                return True

        return False
