import texts
from filters.valid_emal import ValidEmailFilter
from filters.yes_no import YesNoFilter
from handlers import validation
from handlers.common.helpers import Handler
from handlers.start import handlers
from states import StartState, AuthState
from texts import AuthTypes
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.dispatcher.filters.builtin import StateFilter


def prepare_router(dp: Dispatcher):
    message_list = [
        # Start
        Handler(handlers.greeting, [lambda r: r.message.text == "/reset"]),
        Handler(handlers.greeting, [StateFilter(None)]),
        # Greeting
        Handler(
            handlers.introduction,
            [StateFilter(StartState.waiting_greeting), lambda r: r.message.text == texts.HELLO],
        ),
        # # Chose auth type
        Handler(
            handlers.asking_email,
            [
                StateFilter(StartState.waiting_auth_type),
                lambda r: r.message.text == AuthTypes.advanced.value,
            ],
        ),
        Handler(
            handlers.subscription_auth,
            [
                StateFilter(StartState.waiting_auth_type),
                lambda r: r.message.text == AuthTypes.guest.value,
            ],
        ),
        # For advanced auth
        Handler(
            handlers.check_user_email, [StateFilter(AuthState.waiting_email), ValidEmailFilter()]
        ),
        # -> Login handler
        Handler(
            handlers.answer_if_register,
            [StateFilter(AuthState.answering_if_register), YesNoFilter()],
        ),
        # -> Register handler
        # Other questions
        Handler(
            handlers.asking_email,
            [
                StateFilter(AuthState.answering_if_register),
                lambda r: r.message.text == texts.OTHER_MAIL,
            ],
        ),
        Handler(handlers.asking_if_register, [StateFilter(AuthState.answering_if_register)]),
        Handler(
            handlers.answer_if_confirmed_email,
            [StateFilter(AuthState.answering_if_confirmed_email), YesNoFilter()],
        ),
        Handler(
            handlers.start_again,
            [
                StateFilter(AuthState.answering_if_confirmed_email),
                lambda r: r.message.text == texts.START_AGAIN,
            ],
        ),
        Handler(
            handlers.asking_if_email_confirmed,
            [StateFilter(AuthState.answering_if_confirmed_email)],
        ),
        # Validation messages
        Handler(validation.not_valid_email, [StateFilter(AuthState.waiting_email)]),
    ]

    for message in message_list:
        dp.text_messages_handler.subscribe(message.handler, message.filters)
