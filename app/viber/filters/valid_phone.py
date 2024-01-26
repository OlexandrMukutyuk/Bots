import re

from viberio.dispatcher.filters.filters import Filter
from viberio.types.requests import ViberMessageRequest


class ValidPhoneFilter(Filter):
    async def check(self, event):
        if isinstance(event, ViberMessageRequest):
            pattern = "^\\+{0,1}380\\d{9}$"

            if bool(re.match(pattern, event.message.text)):
                return True

        return False
