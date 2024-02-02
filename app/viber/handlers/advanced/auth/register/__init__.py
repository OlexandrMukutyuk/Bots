from filters.strong_password import StrongPasswordFilter
from filters.valid_flat import ValidFlatFilter
from filters.valid_name import ValidNameFilter
from filters.valid_phone import ValidPhoneFilter
from handlers import validation, start
from handlers.advanced.auth.register import register, edit_info
from handlers.common.helpers import Handler
from handlers.start import handlers as start
from keyboards.register import edit_text
from models import Gender
from states import AdvancedRegisterStates, EditRegisterStates
from texts import CHANGE_STREET, WITHOUT_FLAT, AGREEMENT, OTHER_MAIL
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.dispatcher.filters.builtin import StateFilter


def prepare_router(dp: Dispatcher):
    register_message_list = [
        # Get phone
        # Handler(register.save_phone, [AdvancedRegisterStates.waiting_phone, F.contact]),
        Handler(
            register.save_phone,
            [StateFilter(AdvancedRegisterStates.waiting_phone), ValidPhoneFilter()],
        ),
        # Get street
        Handler(
            register.choose_street,
            [
                StateFilter(AdvancedRegisterStates.waiting_street_typing),
                lambda r: len(r.message.text) >= 3,
            ],
        ),
        # Get street
        Handler(
            register.confirm_street,
            [StateFilter(AdvancedRegisterStates.waiting_street_selected)],
        ),
        # Change street
        Handler(
            register.change_street,
            [
                StateFilter(AdvancedRegisterStates.waiting_house),
                lambda r: r.message.text == CHANGE_STREET,
            ],
        ),
        # Get house
        Handler(register.save_house, [StateFilter(AdvancedRegisterStates.waiting_house)]),
        # Get flat
        Handler(
            register.save_flat,
            [StateFilter(AdvancedRegisterStates.waiting_flat), ValidFlatFilter()],
        ),
        Handler(
            register.save_flat,
            [
                StateFilter(AdvancedRegisterStates.waiting_flat),
                lambda r: r.message.text == WITHOUT_FLAT,
            ],
        ),
        # Get first, middle, last Names
        Handler(
            register.save_first_name,
            [StateFilter(AdvancedRegisterStates.waiting_first_name), ValidNameFilter()],
        ),
        Handler(
            register.save_middle_name,
            [StateFilter(AdvancedRegisterStates.waiting_middle_name), ValidNameFilter()],
        ),
        Handler(
            register.save_last_name,
            [StateFilter(AdvancedRegisterStates.waiting_last_name), ValidNameFilter()],
        ),
        # Get gender
        Handler(
            register.save_gender,
            [
                StateFilter(AdvancedRegisterStates.waiting_gender),
                lambda r: r.message.text in Gender.values_reversed.keys(),
            ],
        ),
        # Get password & show agreement
        Handler(
            register.save_password,
            [StateFilter(AdvancedRegisterStates.waiting_password), StrongPasswordFilter()],
        ),
    ]

    edit_message_list = [
        Handler(
            edit_info.send_user_info,
            [
                StateFilter(AdvancedRegisterStates.waiting_agreement),
                lambda r: r.message.text == AGREEMENT,
            ],
        ),
        # Showing typed info
        Handler(
            edit_info.handle_buttons,
            [
                StateFilter(EditRegisterStates.waiting_accepting),
                lambda r: r.message.text in edit_text.values(),
            ],
        ),
        Handler(edit_info.send_user_info, [StateFilter(EditRegisterStates.waiting_accepting)]),
        # Edit info
        Handler(
            edit_info.save_first_name,
            [StateFilter(EditRegisterStates.waiting_first_name), ValidNameFilter()],
        ),
        Handler(
            edit_info.save_middle_name,
            [StateFilter(EditRegisterStates.waiting_middle_name), ValidNameFilter()],
        ),
        Handler(
            edit_info.save_last_name,
            [StateFilter(EditRegisterStates.waiting_last_name), ValidNameFilter()],
        ),
        Handler(
            edit_info.edit_phone,
            [StateFilter(EditRegisterStates.waiting_phone), ValidPhoneFilter()],
        ),
        Handler(
            edit_info.edit_street,
            [
                StateFilter(EditRegisterStates.waiting_street_typing),
                lambda r: len(r.message.text) >= 3,
            ],
        ),
        Handler(edit_info.edit_house, [StateFilter(EditRegisterStates.waiting_house)]),
        Handler(
            edit_info.save_flat, [StateFilter(EditRegisterStates.waiting_flat), ValidFlatFilter()]
        ),
        Handler(
            edit_info.save_flat,
            [
                StateFilter(EditRegisterStates.waiting_flat),
                lambda r: r.message.text == WITHOUT_FLAT,
            ],
        ),
        Handler(
            edit_info.edit_password,
            [StateFilter(EditRegisterStates.waiting_password), StrongPasswordFilter()],
        ),
        # Start again
        Handler(
            start.start_again,
            [
                StateFilter(EditRegisterStates.waiting_email_confirming),
                lambda r: r.message.text == OTHER_MAIL,
            ],
        ),
    ]

    validation_message_list = [
        Handler(validation.not_valid_phone, [StateFilter(AdvancedRegisterStates.waiting_phone)]),
        Handler(validation.not_valid_phone, [StateFilter(EditRegisterStates.waiting_phone)]),
        Handler(
            validation.not_valid_street_name,
            [StateFilter(AdvancedRegisterStates.waiting_street_typing)],
        ),
        Handler(
            validation.not_valid_street_name,
            [StateFilter(EditRegisterStates.waiting_street_typing)],
        ),
        Handler(validation.not_valid_flat, [StateFilter(AdvancedRegisterStates.waiting_flat)]),
        Handler(validation.not_valid_flat, [StateFilter(EditRegisterStates.waiting_flat)]),
        Handler(validation.not_valid_gender, [StateFilter(AdvancedRegisterStates.waiting_gender)]),
        Handler(
            validation.not_valid_first_name,
            [StateFilter(AdvancedRegisterStates.waiting_first_name)],
        ),
        Handler(
            validation.not_valid_last_name,
            [StateFilter(AdvancedRegisterStates.waiting_middle_name)],
        ),
        Handler(
            validation.not_valid_middle_name,
            [StateFilter(AdvancedRegisterStates.waiting_last_name)],
        ),
        Handler(
            validation.not_valid_first_name, [StateFilter(EditRegisterStates.waiting_first_name)]
        ),
        Handler(
            validation.not_valid_last_name, [StateFilter(EditRegisterStates.waiting_middle_name)]
        ),
        Handler(
            validation.not_valid_middle_name, [StateFilter(EditRegisterStates.waiting_last_name)]
        ),
        Handler(validation.weak_password, [StateFilter(AdvancedRegisterStates.waiting_password)]),
        Handler(validation.weak_password, [StateFilter(EditRegisterStates.waiting_password)]),
        Handler(register.show_agreement, [StateFilter(AdvancedRegisterStates.waiting_agreement)]),
    ]

    dp.contact_messages_handler.subscribe(
        register.save_phone, [StateFilter(AdvancedRegisterStates.waiting_phone)]
    )

    dp.contact_messages_handler.subscribe(
        edit_info.edit_phone, [StateFilter(EditRegisterStates.waiting_phone)]
    )

    for message in [*register_message_list, *edit_message_list, *validation_message_list]:
        dp.text_messages_handler.subscribe(message.handler, message.filters)
