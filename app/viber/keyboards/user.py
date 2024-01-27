from keyboards.constructor import KeyboardConstructor
from models import Gender
from texts import BACK

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

edit_profile_kb = KeyboardConstructor.generate_kb(
    buttons=[
        {"Text": edit_text["accept_info_text"], "Columns": 3},
        {"Text": edit_text["first_name_text"], "Columns": 3},
        {"Text": edit_text["last_name_text"], "Columns": 3},
        {"Text": edit_text["middle_name_text"], "Columns": 3},
        {"Text": edit_text["gender_text"], "Columns": 3},
        {"Text": edit_text["street_text"], "Columns": 3},
        {"Text": edit_text["house_text"], "Columns": 3},
        {"Text": edit_text["flat_text"], "Columns": 3},
    ],
    options={"InputFieldState": "hidden"},
)


change_gender_kb = KeyboardConstructor.generate_kb(
    [
        {"Text": Gender.values["male"], "Columns": 3},
        {"Text": Gender.values["female"], "Columns": 3},
        BACK,
    ],
    {"InputFieldState": "hidden"},
)
