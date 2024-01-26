import re

from viberio.dispatcher.filters.filters import Filter
from viberio.types.requests import ViberMessageRequest


class ValidFlatFilter(Filter):
    async def check(self, event):
        if isinstance(event, ViberMessageRequest):
            min = 1
            max = 999

            flat_value = event.message.text

            if flat_value.isdigit() and min <= int(flat_value) <= max:
                return True

        return False
