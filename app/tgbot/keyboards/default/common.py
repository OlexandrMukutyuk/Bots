from keyboards.default.consts import DefaultConstructor
from texts.keyboards import CHANGE_STREET, WITHOUT_FLAT

change_street_kb = DefaultConstructor.create_kb(
    actions=[CHANGE_STREET], schema=[1], one_time_keyboard=True
)


without_flat_kb = DefaultConstructor.create_kb(
    actions=[WITHOUT_FLAT], schema=[1], one_time_keyboard=True
)
