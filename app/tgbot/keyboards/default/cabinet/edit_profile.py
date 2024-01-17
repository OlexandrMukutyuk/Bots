from keyboards.default.consts import DefaultConstructor
from models import Gender
from texts.keyboards import BACK

edit_text = {
    "accept_info_text": "Все вірно ✅",
    "first_name_text": "Ім'я",
    "last_name_text": "Прізвище",
    "middle_name_text": "По батькові",
    "gender_text": "Стать",
    "street_text": "Вулиця",
    "house_text": "Номер будинку",
    "flat_text": "Номер квартири",
}

edit_profile_kb = DefaultConstructor.create_kb(
    actions=[
        edit_text["accept_info_text"],
        edit_text["first_name_text"],
        edit_text["last_name_text"],
        edit_text["middle_name_text"],
        edit_text["gender_text"],
        edit_text["street_text"],
        edit_text["house_text"],
        edit_text["flat_text"],
    ],
    schema=[2, 2, 2, 2],
)


change_gender_kb = DefaultConstructor.create_kb(
    actions=[Gender.values["male"], Gender.values["female"], BACK], schema=[2, 1]
)
