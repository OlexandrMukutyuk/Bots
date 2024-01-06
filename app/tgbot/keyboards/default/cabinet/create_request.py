from aiogram.types import ReplyKeyboardMarkup

from keyboards.default.auth.register import change_street_text
from keyboards.default.auth.start import yes_text, no_text
from keyboards.default.consts import DefaultConstructor

main_menu_text = 'В головне меню'
back_text = 'Назад 🔙'
living_in_house = 'Живу у домі'
no_need = 'Не потрібно ❌'
enough_text = 'Достатньо ✅'
manually_address_text = 'Вписати адресу'
share_geo_text = 'Поділитися геолокацією'

request_back_and_main_kb = DefaultConstructor.create_kb(
    actions=[back_text, main_menu_text],
    schema=[2]
)

request_yes_no_kb = DefaultConstructor.create_kb(
    actions=[yes_text, no_text, back_text, main_menu_text],
    schema=[2, 2]
)

request_house_kb: ReplyKeyboardMarkup = DefaultConstructor.create_kb(
    actions=[change_street_text, main_menu_text],
    schema=[2]
)

request_flat_kb = DefaultConstructor.create_kb(
    actions=[living_in_house, back_text, main_menu_text],
    schema=[2, 1]
)

request_comment_kb = DefaultConstructor.create_kb(
    actions=[back_text, main_menu_text],
    schema=[2]
)

request_images_kb = DefaultConstructor.create_kb(
    actions=[no_need, back_text, main_menu_text],
    schema=[2, 1]
)

request_enough_kb = DefaultConstructor.create_kb(
    actions=[enough_text],
    schema=[1]
)

request_manual_address_kb = DefaultConstructor.create_kb(
    actions=[
        {'text': manually_address_text},
        {'text': share_geo_text, 'location': True},
        {'text': back_text},
        {'text': main_menu_text}
    ],
    schema=[2, 2]
)
