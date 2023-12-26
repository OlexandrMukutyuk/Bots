from aiogram.fsm.state import StatesGroup, State


class StartState(StatesGroup):
    waiting_greeting = State()
    waiting_auth_type = State()


class AuthState(StatesGroup):
    waiting_email = State()
    answering_if_register = State()
    answering_if_confirmed_email = State()


class LoginState(StatesGroup):
    waiting_code = State()


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
