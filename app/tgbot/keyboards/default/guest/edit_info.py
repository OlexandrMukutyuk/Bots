from keyboards.default.consts import DefaultConstructor

edit_text = {
    "accept_info_text": "Все вірно ✅",
    "street_text": "Вулиця ✍",
    "house_text": "Номер будинку ✍",
}


edit_guest_kb = DefaultConstructor.create_kb(
    actions=[edit_text["accept_info_text"], edit_text["street_text"], edit_text["house_text"]],
    schema=[1, 2],
)
