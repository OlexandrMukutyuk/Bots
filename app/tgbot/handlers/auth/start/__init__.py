from aiogram import Router, F
from aiogram.filters import StateFilter, CommandStart

from app.tgbot.filters.valid_emal import ValidEmailFilter
from app.tgbot.keyboards.default.auth.start import yes_text, no_text, start_again_text, auth_types, hello_text, \
    other_mail_text
from app.tgbot.states.auth import StartState, AuthState
from . import handlers
from ... import validation


def prepare_router() -> Router:
    router = Router()

    # Start

    router.message.register(handlers.start, StateFilter(None), CommandStart())

    # Greeting

    router.message.register(handlers.greeting, StartState.waiting_greeting, F.text == hello_text)

    # Chose auth type

    router.message.register(handlers.asking_email, StartState.waiting_auth_type,
                            F.text == auth_types['advanced'])

    router.message.register(handlers.subscription_auth, StartState.waiting_auth_type,
                            F.text == auth_types['subscription'])

    # For advanced auth

    router.message.register(handlers.check_user_email, AuthState.waiting_email, ValidEmailFilter())
    # May -> Login handler

    router.message.register(handlers.answer_if_register, AuthState.answering_if_register,
                            F.text.in_([yes_text, no_text]))
    # May -> Register handler

    # Other questions
    router.message.register(handlers.asking_email, AuthState.answering_if_register, F.text == other_mail_text)
    router.message.register(handlers.asking_if_register, AuthState.answering_if_register)
    router.message.register(handlers.answer_if_confirmed_email, AuthState.answering_if_confirmed_email,
                            F.text.in_([yes_text, no_text]))
    router.message.register(handlers.start_again, AuthState.answering_if_confirmed_email,
                            F.text == start_again_text)
    router.message.register(handlers.asking_if_email_confirmed, AuthState.answering_if_confirmed_email)

    # Validation messages

    router.message.register(validation.not_valid_email, AuthState.waiting_email)

    return router
