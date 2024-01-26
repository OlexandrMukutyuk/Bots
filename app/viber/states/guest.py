from viberio.fsm.states import StatesGroup, State


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

    waiting_email = State()

    # If already register
    waiting_code = State()

    # If not register
    answering_if_register = State()
    answering_if_confirmed_email = State()

    # If not register + want to register
    waiting_phone = State()

    waiting_flat = State()

    waiting_first_name = State()
    waiting_middle_name = State()
    waiting_last_name = State()

    waiting_gender = State()

    waiting_password = State()
    waiting_agreement = State()


class ReferenceInfoStates(StatesGroup):
    waiting_info = State()


class RepairsStates(StatesGroup):
    waiting_address = State()

    waiting_street_typing = State()
    waiting_street_selected = State()

    waiting_house = State()
