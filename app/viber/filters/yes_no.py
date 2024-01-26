from texts import YES, NO
from viberio.dispatcher.filters.filters import Filter
from viberio.types.requests import ViberMessageRequest


class YesNoFilter(Filter):
    async def check(self, event):
        if isinstance(event, ViberMessageRequest):
            if event.message.text in [YES, NO]:
                return True

            return False

        return False
