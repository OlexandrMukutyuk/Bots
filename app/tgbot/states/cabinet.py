from aiogram.fsm.state import StatesGroup, State


class CabinetStates(StatesGroup):
    waiting_menu = State()


class IssueReportStates(StatesGroup):
    waiting_issue_report = State()


class ShareChatbot(StatesGroup):
    waiting_back = State()


class CreateRequest(StatesGroup):
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


class RateEnterprise(StatesGroup):
    showing_list = State()
    enterprise_selected = State()


class ArchiveRequests(StatesGroup):
    waiting_req = State()

    waiting_rate = State()
    waiting_comment = State()


class EditInfo(StatesGroup):
    waiting_first_name = State()
    waiting_middle_name = State()
    waiting_last_name = State()

    waiting_gender = State()
    waiting_street_typing = State()
    waiting_street_selected = State()

    waiting_house = State()
    waiting_flat = State()

    waiting_acception = State()
