from aiogram import Router, F
from aiogram.filters import StateFilter, CommandStart

from filters.valid_emal import ValidEmailFilter
from filters.yes_no import YesNoFilter
from handlers import validation
from handlers.common import Handler
from handlers.start import handlers
from keyboards.default.auth.start import (
    start_again_text,
    auth_types,
    hello_text,
    other_mail_text
)
from states.auth import StartState, AuthState


def prepare_router() -> Router:
    router = Router()

    message_list = [
        # Start
        Handler(handlers.greeting, [StateFilter(None), CommandStart()]),

        # Greeting
        Handler(handlers.introduction, [StartState.waiting_greeting, F.text == hello_text]),

        # Chose auth type
        Handler(handlers.asking_email, [StartState.waiting_auth_type, F.text == auth_types['advanced']]),
        Handler(handlers.subscription_auth, [StartState.waiting_auth_type, F.text == auth_types['subscription']]),

        # For advanced auth
        Handler(handlers.check_user_email, [AuthState.waiting_email, ValidEmailFilter()]),
        # -> Login handler
        Handler(handlers.answer_if_register, [AuthState.answering_if_register, YesNoFilter()]),
        # -> Register handler

        # Other questions
        Handler(handlers.asking_email, [AuthState.answering_if_register, F.text == other_mail_text]),
        Handler(handlers.asking_if_register, [AuthState.answering_if_register]),
        Handler(handlers.answer_if_confirmed_email, [AuthState.answering_if_confirmed_email, YesNoFilter()]),
        Handler(handlers.start_again, [AuthState.answering_if_confirmed_email, F.text == start_again_text]),
        Handler(handlers.asking_if_email_confirmed, [AuthState.answering_if_confirmed_email]),

        # Validation messages
        Handler(validation.not_valid_email, [AuthState.waiting_email]),
    ]

    for message in message_list:
        router.message.register(message.handler, *message.filters)

    return router
