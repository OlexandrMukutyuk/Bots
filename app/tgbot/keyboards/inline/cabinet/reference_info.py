from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.inline.callbacks import EnterpriseCallbackFactory, EnterpriseRateCallbackFactory, \
    ReferenceInfoCallbackFactory
from texts.keyboards import BACK, TO_MENU


def generate_ref_info_kb(ref_info: list[dict]):
    builder = InlineKeyboardBuilder()

    for item in ref_info:
        builder.button(
            text=item.get("Title"),
            callback_data=ReferenceInfoCallbackFactory(id=item.get("Id")),
        )

    builder.button(text=TO_MENU, callback_data="to_menu")

    builder.adjust(2)

    return builder.as_markup()

