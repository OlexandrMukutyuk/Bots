from texts import YES
from viberio.dispatcher.filters.filters import Filter
from viberio.types.requests import ViberMessageRequest


class YesFilter(Filter):
    async def check(self, event):
        if isinstance(event, ViberMessageRequest):
            if event.message.text == YES:
                return True

        return False
