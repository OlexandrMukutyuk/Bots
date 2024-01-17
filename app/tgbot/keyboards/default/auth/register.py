from keyboards.default.consts import DefaultConstructor
from models import Gender
from texts.keyboards import SHARE_CONTACT, AGREEMENT


phone_share_kb = DefaultConstructor.create_kb(
    actions=[{"text": SHARE_CONTACT, "contact": True}], schema=[1], one_time_keyboard=True
)


choose_gender_kb = DefaultConstructor.create_kb(
    actions=[*list(Gender.values_reversed.keys())], schema=[2, 1], one_time_keyboard=True
)

registration_agreement_kb = DefaultConstructor.create_kb(actions=[AGREEMENT], schema=[1])
