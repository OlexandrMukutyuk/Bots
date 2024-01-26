from handlers.advanced.auth.login import handlers
from states import LoginState
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.dispatcher.filters.builtin import StateFilter


def prepare_router(dp: Dispatcher):
    dp.text_messages_handler.subscribe(
        handlers.check_email_code, [StateFilter(LoginState.waiting_code)]
    )
