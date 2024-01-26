from viberio.fsm.states import StatesGroup, State


class StartState(StatesGroup):
    waiting_greeting = State()
    waiting_auth_type = State()
