from app.tgbot.keyboards.default.consts import DefaultConstructor

gender_dict = {
    "male": "Чоловік",
    "female": "Жінка",
    "other": "Не хочу вказувати"
}

change_street_text: str = 'Змінити вулицю'
without_flat_text: str = "Передавати номер квартири не потрібно"
agreement_text: str = "Погоджуюсь ✅"

phone_share_kb = DefaultConstructor.create_kb(
    actions=[{"text": 'Поділитись телефоном', 'contact': True}],
    schema=[1],
    one_time_keyboard=True
)

change_street_kb = DefaultConstructor.create_kb(
    actions=[change_street_text],
    schema=[1],
    one_time_keyboard=True
)

without_flat_kb = DefaultConstructor.create_kb(
    actions=[without_flat_text],
    schema=[1],
    one_time_keyboard=True
)

choose_gender_kb = DefaultConstructor.create_kb(
    actions=[gender_dict['male'], gender_dict['female'], gender_dict['other']],
    schema=[2, 1],
    one_time_keyboard=True
)

registration_agreement_kb = DefaultConstructor.create_kb(
    actions=[agreement_text],
    schema=[1],
    one_time_keyboard=True
)
