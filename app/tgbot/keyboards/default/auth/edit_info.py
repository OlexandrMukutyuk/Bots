from keyboards.default.consts import DefaultConstructor

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

edit_register_info_kb = DefaultConstructor.create_kb(
    actions=[
        edit_text['accept_info_text'],
        edit_text['first_name_text'],
        edit_text['last_name_text'],
        edit_text['middle_name_text'],
        edit_text['phone_text'],
        edit_text['street_text'],
        edit_text['house_text'],
        edit_text['flat_text'],
        edit_text['password_text']
    ],
    schema=[2, 2, 2, 2, 1]
)
