from aiogram import Router, F
from aiogram.filters import CommandStart

import texts
from filters.valid_emal import ValidEmailFilter
from filters.yes_no import YesNoFilter
from handlers import validation
from handlers.common.helpers import Handler
from handlers.start import handlers
from states.advanced import AuthState
from states.start import StartState
from texts import AuthTypes


def prepare_router() -> Router:
    router = Router()

    message_list = [
        # Start
        Handler(handlers.greeting, [CommandStart()]),
        # Greeting
        Handler(handlers.introduction, [StartState.waiting_greeting, F.text == texts.HELLO]),
        # Chose auth type
        Handler(
            handlers.asking_email,
            [StartState.waiting_auth_type, F.text == AuthTypes.advanced.value],
        ),
        Handler(
            handlers.subscription_auth,
            [StartState.waiting_auth_type, F.text == AuthTypes.guest.value],
        ),
        # For advanced auth
        Handler(handlers.check_user_email, [AuthState.waiting_email, ValidEmailFilter()]),
        # -> Login handler
        Handler(handlers.answer_if_register, [AuthState.answering_if_register, YesNoFilter()]),
        # -> Register handler
        # Other questions
        Handler(
            handlers.asking_email, [AuthState.answering_if_register, F.text == texts.OTHER_MAIL]
        ),
        Handler(handlers.asking_if_register, [AuthState.answering_if_register]),
        Handler(
            handlers.answer_if_confirmed_email,
            [AuthState.answering_if_confirmed_email, YesNoFilter()],
        ),
        Handler(
            handlers.start_again,
            [AuthState.answering_if_confirmed_email, F.text == texts.START_AGAIN],
        ),
        Handler(handlers.asking_if_email_confirmed, [AuthState.answering_if_confirmed_email]),
        # Validation messages
        Handler(validation.not_valid_email, [AuthState.waiting_email]),
    ]

    for message in message_list:
        router.message.register(message.handler, *message.filters)

    return router
