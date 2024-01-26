from texts import YES, NO, BACK
from viberio.dispatcher.filters.filters import Filter
from viberio.types.requests import ViberMessageRequest


class BackFilter(Filter):
    async def check(self, event):
        if isinstance(event, ViberMessageRequest):
            if event.message.text == BACK:
                return True


        return False
