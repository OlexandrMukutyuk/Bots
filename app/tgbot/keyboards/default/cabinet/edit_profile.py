from app.tgbot.keyboards.default.auth.register import gender_dict
from app.tgbot.keyboards.default.cabinet.create_request import back_text
from app.tgbot.keyboards.default.consts import DefaultConstructor

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
        edit_text['accept_info_text'],
        edit_text['first_name_text'],
        edit_text['last_name_text'],
        edit_text['middle_name_text'],
        edit_text['gender_text'],
        edit_text['street_text'],
        edit_text['house_text'],
        edit_text['flat_text']
    ],
    schema=[2, 2, 2, 2]
)

back_kb = DefaultConstructor.create_kb(
    actions=[back_text],
    schema=[1]
)

change_gender_kb = DefaultConstructor.create_kb(
    actions=[gender_dict['male'], gender_dict['female'], back_text],
    schema=[2, 1]
)
