from keyboards.inline.callbacks import StreetCallbackFactory
from keyboards.inline.consts import InlineConstructor

choose_street_kb = InlineConstructor.create_kb(
    actions=[{
        "text": "Обрати вулицю",
        "switch_inline_query_current_chat": "streets_for_carousel"
    }],
    schema=[1]
)


def confirm_street_kb(street_id: int, city_id: int):
    return InlineConstructor.create_kb(
        actions=[{
            "text": "Вибрати ✅",
            "callback_data": StreetCallbackFactory(street_id=street_id, city_id=city_id)
        }],
        schema=[1]
    )
