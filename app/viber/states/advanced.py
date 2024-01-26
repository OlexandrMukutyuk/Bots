from viberio.fsm.states import StatesGroup, State


class AuthState(StatesGroup):
    waiting_email = State()
    answering_if_register = State()
    answering_if_confirmed_email = State()


class LoginState(StatesGroup):
    waiting_code = State()


class AdvancedRegisterStates(StatesGroup):
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


class EditRegisterStates(StatesGroup):
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

    waiting_email_confirming = State()


class FullCabinetStates(StatesGroup):
    waiting_menu = State()


class FullIssueReportStates(StatesGroup):
    waiting_issue_report = State()


class FullShareChatbotStates(StatesGroup):
    waiting_back = State()


class CreateRequestStates(StatesGroup):
    waiting_problem = State()
    waiting_reason = State()

    waiting_address = State()

    is_address_manually = State()
    share_geo = State()

    waiting_street_typing = State()
    waiting_street_selected = State()
    waiting_house = State()

    waiting_flat = State()
    waiting_comment = State()
    waiting_showing_status = State()
    waiting_images = State()
    waiting_images_more = State()

    waiting_confirm = State()


class FullRateEnterpriseStates(StatesGroup):
    showing_list = State()
    enterprise_selected = State()


class ArchiveRequestsStates(StatesGroup):
    waiting_req = State()

    waiting_rate = State()
    waiting_comment = State()


class FullEditInfoStates(StatesGroup):
    waiting_first_name = State()
    waiting_middle_name = State()
    waiting_last_name = State()

    waiting_gender = State()
    waiting_street_typing = State()
    waiting_street_selected = State()

    waiting_house = State()
    waiting_flat = State()

    waiting_acceptation = State()


class FullReferenceInfoStates(StatesGroup):
    waiting_info = State()


class FullRepairsStates(StatesGroup):
    waiting_address = State()

    waiting_street_typing = State()
    waiting_street_selected = State()

    waiting_house = State()
