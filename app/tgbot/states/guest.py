from aiogram.fsm.state import StatesGroup, State


class GuestAuthStates(StatesGroup):
    waiting_street_typing = State()
    waiting_street_selected = State()

    waiting_house = State()


class GuestCabinetStates(StatesGroup):
    waiting_menu = State()
    waiting_issue_report = State()


class GuestEditInfoStates(StatesGroup):
    waiting_street_typing = State()
    waiting_street_selected = State()

    waiting_house = State()

    waiting_acceptation = State()


class GuestRateEnterpriseStates(StatesGroup):
    showing_list = State()
    enterprise_selected = State()


class GuestShareBotStates(StatesGroup):
    waiting_back = State()


class GuestFullRegisterStates(StatesGroup):
    waiting_answer = State()
