from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.inline.callbacks import EnterpriseCallbackFactory, EnterpriseRateCallbackFactory
from texts.keyboards import BACK


def enterprises_list_kb(enterprises: list[dict]):
    builder = InlineKeyboardBuilder()

    for item in enterprises:
        builder.button(
            text=item.get("Name"),
            callback_data=EnterpriseCallbackFactory(enterprise_id=item.get("Id")),
        )

    builder.button(text=BACK, callback_data="back")

    builder.adjust(1)

    return builder.as_markup()


def enterprises_rates_kb(enterprise_id: int):
    builder = InlineKeyboardBuilder()

    rates = [5, 4, 3, 2, 1]

    for rate in rates:
        builder.button(
            text=f"{rate} ⭐",
            callback_data=EnterpriseRateCallbackFactory(rate=rate, enterprise_id=enterprise_id),
        )

    builder.button(text=BACK, callback_data="back")

    builder.adjust(1)

    return builder.as_markup()
