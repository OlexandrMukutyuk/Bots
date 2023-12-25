from aiogram.fsm.state import StatesGroup, State


class AdvancedRegisterState(StatesGroup):
    waiting_phone = State()
    waiting_street_typing = State()

    waiting_street_selected = State()

    waiting_house = State()
    waiting_flat = State()

    waiting_first_name = State()
    waiting_middle_name = State()
    waiting_last_name = State()

    waiting_gender = State()

    waiting_password = State()
    waiting_agreement = State()


class EditRegisterState(StatesGroup):
    waiting_first_name = State()
    waiting_middle_name = State()
    waiting_last_name = State()

    waiting_phone = State()
    waiting_street_typing = State()
    waiting_street_selected = State()

    waiting_house = State()
    waiting_flat = State()

    waiting_password = State()
    waiting_accepting = State()
