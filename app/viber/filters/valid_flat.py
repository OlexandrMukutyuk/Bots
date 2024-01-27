from texts import WITHOUT_FLAT
from viberio.dispatcher.filters.filters import Filter
from viberio.types.requests import ViberMessageRequest


class ValidFlatFilter(Filter):
    async def check(self, event):
        if isinstance(event, ViberMessageRequest):
            flat_value = event.message.text

            print(flat_value)
            if flat_value == WITHOUT_FLAT:
                return True

            min = 1
            max = 999

            if flat_value.isdigit() and min <= int(flat_value) <= max:
                return True

        return False
