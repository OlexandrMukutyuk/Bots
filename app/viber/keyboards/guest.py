from keyboards.constructor import KeyboardConstructor

edit_text = {
    "accept_info_text": "Все вірно ✅",
    "street_text": "Вулиця ✍",
    "house_text": "Номер будинку ✍",
}


edit_guest_kb = KeyboardConstructor.generate_kb(
    buttons=[
        {"Text": edit_text["accept_info_text"], "Columns": 6, "Rows": 1},
        {"Text": edit_text["street_text"], "Columns": 3, "Rows": 1},
        {"Text": edit_text["house_text"], "Columns": 3, "Rows": 1},
    ],
    options={"InputFieldState": "hidden"},
)
