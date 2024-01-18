from aiogram.types import ReplyKeyboardMarkup

from keyboards.default.consts import DefaultConstructor
from keyboards.default.start import YES, NO
from texts.keyboards import (
    CHANGE_STREET,
    BACK,
    TO_MAIN_MENU,
    LIVING_IN_HOUSE,
    NO_NEED,
    ENOUGH,
    SHARE_GEO,
    MANUALLY_ADDRESS,
)

request_back_and_main_kb = DefaultConstructor.create_kb(actions=[BACK, TO_MAIN_MENU], schema=[2])

request_yes_no_kb = DefaultConstructor.create_kb(
    actions=[YES, NO, BACK, TO_MAIN_MENU], schema=[2, 2]
)

request_house_kb: ReplyKeyboardMarkup = DefaultConstructor.create_kb(
    actions=[CHANGE_STREET, TO_MAIN_MENU], schema=[2]
)

request_flat_kb = DefaultConstructor.create_kb(
    actions=[LIVING_IN_HOUSE, BACK, TO_MAIN_MENU], schema=[2, 1]
)

request_comment_kb = DefaultConstructor.create_kb(actions=[BACK, TO_MAIN_MENU], schema=[2])

request_images_kb = DefaultConstructor.create_kb(
    actions=[NO_NEED, BACK, TO_MAIN_MENU], schema=[2, 1]
)

request_enough_kb = DefaultConstructor.create_kb(actions=[ENOUGH], schema=[1])

request_manual_address_kb = DefaultConstructor.create_kb(
    actions=[
        {"text": MANUALLY_ADDRESS},
        {"text": SHARE_GEO, "location": True},
        {"text": BACK},
        {"text": TO_MAIN_MENU},
    ],
    schema=[2, 2],
)
