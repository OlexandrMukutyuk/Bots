from aiogram.filters.callback_data import CallbackData


class StreetCallbackFactory(CallbackData, prefix="user_street"):
    street_id: int
    city_id: int
