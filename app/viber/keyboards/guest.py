import texts
from keyboards.constructor import KeyboardConstructor
from texts import START_FULL_REGISTRATION, GO_BACK

edit_text = {
    "accept_info_text": "Все вірно ✅",
    "street_text": "Вулиця ✍",
    "house_text": "Номер будинку ✍",
}


edit_guest_kb = KeyboardConstructor.generate_kb(
    buttons=[
        {"Text": edit_text["accept_info_text"], "Columns": 6, "Color": texts.GREEN},
        {"Text": edit_text["street_text"], "Columns": 3},
        {"Text": edit_text["house_text"], "Columns": 3},
    ],
    options={"InputFieldState": "hidden"},
)


full_registration_kb = KeyboardConstructor.generate_kb(
    [
        {"Text": START_FULL_REGISTRATION, "Columns": 3, "Color": texts.RED},
        {"Text": GO_BACK, "Columns": 3},
    ],
    {"InputFieldState": "hidden"},
)
