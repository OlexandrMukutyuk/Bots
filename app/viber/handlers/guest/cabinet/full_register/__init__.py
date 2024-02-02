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
from texts import AGREEMENT
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.dispatcher.filters.builtin import StateFilter


def prepare_router(dp: Dispatcher):
    last_chance_list = [
        Handler(
            menu.show_cabinet_menu,
            [
                StateFilter(GuestFullRegisterStates.waiting_answer),
                lambda r: r.message.text == texts.GO_BACK,
            ],
        ),
        Handler(
            start.asking_email,
            [
                StateFilter(GuestFullRegisterStates.waiting_answer),
                lambda r: r.message.text == texts.START_FULL_REGISTRATION,
            ],
        ),
        Handler(menu.full_registration, [StateFilter(GuestFullRegisterStates.waiting_answer)]),
    ]

    checking_email_list = [
        Handler(
            start.check_user_email,
            [StateFilter(GuestFullRegisterStates.waiting_email), ValidEmailFilter()],
        ),
        Handler(
            start.answer_if_register,
            [StateFilter(GuestFullRegisterStates.answering_if_register), YesNoFilter()],
        ),
        Handler(
            start.asking_email,
            [
                StateFilter(GuestFullRegisterStates.answering_if_register),
                lambda r: r.message.text == texts.OTHER_MAIL,
            ],
        ),
        Handler(
            start.asking_if_register, [StateFilter(GuestFullRegisterStates.answering_if_register)]
        ),
        Handler(
            start.answer_if_confirmed_email,
            [StateFilter(GuestFullRegisterStates.answering_if_confirmed_email), YesNoFilter()],
        ),
        Handler(
            start.start_again,
            [
                StateFilter(GuestFullRegisterStates.answering_if_confirmed_email),
                lambda r: r.messagetext == texts.START_AGAIN,
            ],
        ),
    ]

    login_handlers = [
        Handler(start.check_email_code, [StateFilter(GuestFullRegisterStates.waiting_code)])
    ]

    register_message_list = [
        # Get phone
        Handler(
            register.save_phone,
            [StateFilter(GuestFullRegisterStates.waiting_phone), ValidPhoneFilter()],
        ),
        # Get flat
        Handler(
            register.save_flat,
            [StateFilter(GuestFullRegisterStates.waiting_flat), ValidFlatFilter()],
        ),
        # Get first, middle, last Names
        Handler(
            register.save_first_name,
            [StateFilter(GuestFullRegisterStates.waiting_first_name), ValidNameFilter()],
        ),
        Handler(
            register.save_middle_name,
            [StateFilter(GuestFullRegisterStates.waiting_middle_name), ValidNameFilter()],
        ),
        Handler(
            register.save_last_name,
            [StateFilter(GuestFullRegisterStates.waiting_last_name), ValidNameFilter()],
        ),
        # Get gender
        Handler(
            register.save_gender,
            [
                StateFilter(GuestFullRegisterStates.waiting_gender),
                lambda r: r.message.text in Gender.values_reversed.keys(),
            ],
        ),
        # Get password & show agreement
        Handler(
            register.save_password,
            [StateFilter(GuestFullRegisterStates.waiting_password), StrongPasswordFilter()],
        ),
    ]

    edit_handlers = [
        Handler(
            edit_info.send_user_info,
            [
                StateFilter(GuestFullRegisterStates.waiting_agreement),
                lambda r: r.message.text == AGREEMENT,
            ],
        ),
    ]

    validation_message_list = [
        # Start
        Handler(
            start.asking_if_register, [StateFilter(GuestFullRegisterStates.answering_if_register)]
        ),
        Handler(
            start.asking_if_email_confirmed,
            [StateFilter(GuestFullRegisterStates.answering_if_confirmed_email)],
        ),
        Handler(validation.not_valid_email, [StateFilter(GuestFullRegisterStates.waiting_email)]),
        # Register
        Handler(validation.not_valid_phone, [StateFilter(GuestFullRegisterStates.waiting_phone)]),
        Handler(validation.not_valid_flat, [StateFilter(GuestFullRegisterStates.waiting_flat)]),
        Handler(validation.not_valid_gender, [StateFilter(GuestFullRegisterStates.waiting_gender)]),
        Handler(
            validation.not_valid_first_name,
            [StateFilter(GuestFullRegisterStates.waiting_first_name)],
        ),
        Handler(
            validation.not_valid_last_name,
            [StateFilter(GuestFullRegisterStates.waiting_middle_name)],
        ),
        Handler(
            validation.not_valid_middle_name,
            [StateFilter(GuestFullRegisterStates.waiting_last_name)],
        ),
        Handler(validation.weak_password, [StateFilter(GuestFullRegisterStates.waiting_password)]),
        Handler(register.show_agreement, [StateFilter(GuestFullRegisterStates.waiting_agreement)]),
    ]

    dp.contact_messages_handler.subscribe(
        register.save_phone, [StateFilter(GuestFullRegisterStates.waiting_phone)]
    )

    for message in [
        *last_chance_list,
        *checking_email_list,
        *login_handlers,
        *register_message_list,
        *edit_handlers,
        *validation_message_list,
    ]:
        dp.text_messages_handler.subscribe(message.handler, message.filters)
