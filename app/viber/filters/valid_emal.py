import re

from viberio.dispatcher.filters.filters import Filter
from viberio.types.requests import ViberMessageRequest


class ValidEmailFilter(Filter):
    async def check(self, event):
        if isinstance(event, ViberMessageRequest):
            pattern = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"

            if bool(re.match(pattern, event.message.text)):
                return True


        return False
