from aiogram.fsm.state import StatesGroup, State


class AuthStates(StatesGroup):
    waiting_street_typing = State()
    waiting_street_selected = State()

    waiting_house = State()


class SubscribeCabinet(StatesGroup):
    waiting_menu = State()
    waiting_issue_report = State()


class RateEnterpriseStates(StatesGroup):
    showing_list = State()
    enterprise_selected = State()


class SubscribeShareBot(StatesGroup):
    waiting_back = State()
