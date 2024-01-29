import texts
from keyboards.constructor import KeyboardConstructor
from texts import SHARE_CONTACT, AGREEMENT

phone_share_kb = KeyboardConstructor.generate_kb(
    [
        {"Text": SHARE_CONTACT, "ActionType": "share-phone", "Columns": 6, "Rows": 1},
    ]
)


registration_agreement_kb = KeyboardConstructor.generate_kb([AGREEMENT])


edit_text = {
    "accept_info_text": "Все вірно ✅",
    "first_name_text": "Ім'я",
    "last_name_text": "Прізвище",
    "middle_name_text": "По батькові",
    "phone_text": "Телефон",
    "street_text": "Вулиця",
    "house_text": "Номер будинку",
    "flat_text": "Номер квартири",
    "password_text": "Пароль",
}

edit_register_info_kb = KeyboardConstructor.generate_kb(
    [
        {"Text": edit_text["accept_info_text"], "Columns": 6, "Color": texts.GREEN},
        {"Text": edit_text["first_name_text"], "Columns": 3},
        {"Text": edit_text["last_name_text"], "Columns": 3},
        {"Text": edit_text["middle_name_text"], "Columns": 3},
        {"Text": edit_text["phone_text"], "Columns": 3},
        {"Text": edit_text["street_text"], "Columns": 3},
        {"Text": edit_text["house_text"], "Columns": 3},
        {"Text": edit_text["flat_text"], "Columns": 3},
        {"Text": edit_text["password_text"], "Columns": 3},
    ],
    {"InputFieldState": "hidden"},
)
