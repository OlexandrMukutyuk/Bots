from texts import NO
from viberio.dispatcher.filters.filters import Filter
from viberio.types.requests import ViberMessageRequest


class NoFilter(Filter):
    async def check(self, event):
        if isinstance(event, ViberMessageRequest):
            if event.message.text == NO:
                return True

        return False
