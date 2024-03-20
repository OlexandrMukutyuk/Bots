from keyboards.default.consts import DefaultConstructor
from models import Gender
from texts.keyboards import SHARE_CONTACT, AGREEMENT, REGION_KH, REGION_OTHER

phone_share_kb = DefaultConstructor.create_kb(
    actions=[{"text": SHARE_CONTACT, "contact": True}], schema=[1]
)

choose_gender_kb = DefaultConstructor.create_kb(
    actions=[*list(Gender.values_reversed.keys())], schema=[2, 1], one_time_keyboard=True
)

choice_region_item = {
    "region_kh": REGION_KH,
    "region_other": REGION_OTHER,
}

choice_region_kb = DefaultConstructor.create_kb(
    actions=[REGION_KH, REGION_OTHER], schema=[2]
)

other_location_kb = DefaultConstructor.create_kb(
    actions=['Мого населений пункту немає в списку'], schema=[1]
)

registration_agreement_kb = DefaultConstructor.create_kb(actions=[AGREEMENT], schema=[1])
