from aiogram import Router, F

import texts
from filters.strong_password import StrongPasswordFilter
from filters.valid_emal import ValidEmailFilter
from filters.valid_flat import ValidFlatFilter
from filters.valid_name import ValidNameFilter
from filters.valid_phone import ValidPhoneFilter
from filters.yes_no import YesNoFilter
from handlers import validation
from handlers.advanced.auth.register import edit_info
from handlers.common.helpers import Handler
from handlers.guest.cabinet.full_register import register_handlers as register
from handlers.guest.cabinet.full_register import start_handlers as start
from handlers.guest.cabinet.menu import handlers as menu
from models import Gender
from states import GuestFullRegisterStates
from texts import AGREEMENT, WITHOUT_FLAT


def prepare_router() -> Router:
    router = Router()

    last_chance_list = [
        Handler(
            menu.show_cabinet_menu,
            [GuestFullRegisterStates.waiting_answer, F.text == texts.GO_BACK],
        ),
        Handler(
            start.asking_email,
            [GuestFullRegisterStates.waiting_answer, F.text == texts.START_FULL_REGISTRATION],
        ),
        Handler(menu.full_registration, [GuestFullRegisterStates.waiting_answer]),
    ]

    checking_email_list = [
        Handler(
            start.check_user_email, [GuestFullRegisterStates.waiting_email, ValidEmailFilter()]
        ),
        Handler(
            start.answer_if_register,
            [GuestFullRegisterStates.answering_if_register, YesNoFilter()],
        ),
        Handler(
            start.asking_email,
            [GuestFullRegisterStates.answering_if_register, F.text == texts.OTHER_MAIL],
        ),
        Handler(start.asking_if_register, [GuestFullRegisterStates.answering_if_register]),
        Handler(
            start.answer_if_confirmed_email,
            [GuestFullRegisterStates.answering_if_confirmed_email, YesNoFilter()],
        ),
        Handler(
            start.start_again,
            [GuestFullRegisterStates.answering_if_confirmed_email, F.text == texts.START_AGAIN],
        ),
    ]

    login_handlers = [Handler(start.check_email_code, [GuestFullRegisterStates.waiting_code])]

    register_message_list = [
        # Get phone
        Handler(register.save_phone, [GuestFullRegisterStates.waiting_phone, F.contact]),
        Handler(register.save_phone, [GuestFullRegisterStates.waiting_phone, ValidPhoneFilter()]),
        # Get flat
        Handler(register.save_flat, [GuestFullRegisterStates.waiting_flat, ValidFlatFilter()]),
        Handler(register.save_flat, [GuestFullRegisterStates.waiting_flat, F.text == WITHOUT_FLAT]),
        # Get first, middle, last Names
        Handler(
            register.save_first_name,
            [GuestFullRegisterStates.waiting_first_name, ValidNameFilter()],
        ),
        Handler(
            register.save_middle_name,
            [GuestFullRegisterStates.waiting_middle_name, ValidNameFilter()],
        ),
        Handler(
            register.save_last_name, [GuestFullRegisterStates.waiting_last_name, ValidNameFilter()]
        ),
        # Get gender
        Handler(
            register.save_gender,
            [GuestFullRegisterStates.waiting_gender, F.text.in_(Gender.values_reversed.keys())],
        ),
        # Get password & show agreement
        Handler(
            register.save_password,
            [GuestFullRegisterStates.waiting_password, StrongPasswordFilter()],
        ),
        Handler(
            register.show_agreement, [GuestFullRegisterStates.waiting_password, F.text != AGREEMENT]
        ),
    ]

    edit_handlers = [
        Handler(
            edit_info.first_time_showing_user_info,
            [GuestFullRegisterStates.waiting_agreement, F.text == AGREEMENT],
        ),
    ]

    validation_message_list = [
        # Start
        Handler(start.asking_if_register, [GuestFullRegisterStates.answering_if_register]),
        Handler(
            start.asking_if_email_confirmed,
            [GuestFullRegisterStates.answering_if_confirmed_email],
        ),
        Handler(validation.not_valid_email, [GuestFullRegisterStates.waiting_email]),
        # Register
        Handler(validation.not_valid_phone, [GuestFullRegisterStates.waiting_phone]),
        Handler(validation.not_valid_flat, [GuestFullRegisterStates.waiting_flat]),
        Handler(validation.not_valid_gender, [GuestFullRegisterStates.waiting_gender]),
        Handler(validation.not_valid_first_name, [GuestFullRegisterStates.waiting_first_name]),
        Handler(validation.not_valid_last_name, [GuestFullRegisterStates.waiting_middle_name]),
        Handler(validation.not_valid_middle_name, [GuestFullRegisterStates.waiting_last_name]),
        Handler(validation.weak_password, [GuestFullRegisterStates.waiting_password]),
        Handler(register.show_agreement, [GuestFullRegisterStates.waiting_agreement]),
    ]

    for message in [
        *last_chance_list,
        *checking_email_list,
        *login_handlers,
        *register_message_list,
        *edit_handlers,
        *validation_message_list,
    ]:
        router.message.register(message.handler, *message.filters)

    return router
