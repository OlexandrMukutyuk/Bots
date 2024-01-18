from aiogram import Router, F

from filters.strong_password import StrongPasswordFilter
from filters.valid_flat import ValidFlatFilter
from filters.valid_name import ValidNameFilter
from filters.valid_phone import ValidPhoneFilter
from handlers import validation
from handlers.advanced.auth.register import edit_info
from handlers.advanced.auth.register import register
from handlers.common.helpers import Handler
from handlers.common.streets import StreetsHandlers
from handlers.start import handlers as start
from keyboards.default.auth.edit_info import edit_text
from keyboards.inline.callbacks import StreetCallbackFactory
from models import Gender
from states.advanced import AdvancedRegisterStates, EditRegisterStates
from texts.keyboards import CHANGE_STREET, AGREEMENT, WITHOUT_FLAT


def prepare_router() -> Router:
    router = Router()

    register_message_list = [
        # Get phone
        Handler(register.save_phone, [AdvancedRegisterStates.waiting_phone, F.contact]),
        Handler(register.save_phone, [AdvancedRegisterStates.waiting_phone, ValidPhoneFilter()]),
        # Get street
        Handler(
            register.choose_street,
            [AdvancedRegisterStates.waiting_street_typing, F.text.len() >= 3],
        ),
        Handler(
            StreetsHandlers.message_via_bot,
            [AdvancedRegisterStates.waiting_street_selected, F.via_bot],
        ),
        Handler(
            register.choose_street,
            [AdvancedRegisterStates.waiting_street_selected, F.text.len() >= 3, ~F.via_bot],
        ),
        # Change street
        Handler(
            register.change_street, [AdvancedRegisterStates.waiting_house, F.text == CHANGE_STREET]
        ),
        # Get house
        Handler(register.save_house, [AdvancedRegisterStates.waiting_house]),
        # Get flat
        Handler(register.save_flat, [AdvancedRegisterStates.waiting_flat, ValidFlatFilter()]),
        Handler(register.save_flat, [AdvancedRegisterStates.waiting_flat, F.text == WITHOUT_FLAT]),
        # Get first, middle, last Names
        Handler(
            register.save_first_name, [AdvancedRegisterStates.waiting_first_name, ValidNameFilter()]
        ),
        Handler(
            register.save_middle_name,
            [AdvancedRegisterStates.waiting_middle_name, ValidNameFilter()],
        ),
        Handler(
            register.save_last_name, [AdvancedRegisterStates.waiting_last_name, ValidNameFilter()]
        ),
        # Get gender
        Handler(
            register.save_gender,
            [AdvancedRegisterStates.waiting_gender, F.text.in_(Gender.values_reversed.keys())],
        ),
        # Get password & show agreement
        Handler(
            register.save_password,
            [AdvancedRegisterStates.waiting_password, StrongPasswordFilter()],
        ),
    ]

    edit_message_list = [
        Handler(
            edit_info.first_time_showing_user_info,
            [AdvancedRegisterStates.waiting_agreement, F.text == AGREEMENT],
        ),
        # Showing typed info
        Handler(
            edit_info.handle_buttons,
            [EditRegisterStates.waiting_accepting, F.text.in_(edit_text.values())],
        ),
        Handler(edit_info.first_time_showing_user_info, [EditRegisterStates.waiting_accepting]),
        # Edit info
        Handler(
            edit_info.edit_first_name, [EditRegisterStates.waiting_first_name, ValidNameFilter()]
        ),
        Handler(
            edit_info.edit_middle_name, [EditRegisterStates.waiting_middle_name, ValidNameFilter()]
        ),
        Handler(
            edit_info.edit_last_name, [EditRegisterStates.waiting_last_name, ValidNameFilter()]
        ),
        Handler(edit_info.edit_phone, [EditRegisterStates.waiting_phone, F.contact]),
        Handler(edit_info.edit_phone, [EditRegisterStates.waiting_phone, ValidPhoneFilter()]),
        Handler(
            edit_info.edit_street, [EditRegisterStates.waiting_street_typing, F.text.len() >= 3]
        ),
        Handler(
            edit_info.edit_street,
            [EditRegisterStates.waiting_street_selected, F.text.len() >= 3, ~F.via_bot],
        ),
        Handler(
            StreetsHandlers.message_via_bot,
            [EditRegisterStates.waiting_street_selected, F.via_bot],
        ),
        Handler(edit_info.edit_house, [EditRegisterStates.waiting_house]),
        Handler(edit_info.edit_flat, [EditRegisterStates.waiting_flat, ValidFlatFilter()]),
        Handler(edit_info.edit_flat, [EditRegisterStates.waiting_flat, F.text == WITHOUT_FLAT]),
        Handler(
            edit_info.edit_password, [EditRegisterStates.waiting_password, StrongPasswordFilter()]
        ),
        # Start again
        Handler(start.start_again, [EditRegisterStates.waiting_email_confirming]),
    ]

    inline_list = [
        Handler(register.show_street_list, [AdvancedRegisterStates.waiting_street_selected]),
        Handler(edit_info.show_street_list, [EditRegisterStates.waiting_street_selected]),
    ]

    callback_list = [
        Handler(
            register.confirm_street,
            [StreetCallbackFactory.filter(), AdvancedRegisterStates.waiting_street_selected],
        ),
        Handler(
            edit_info.confirm_street,
            [StreetCallbackFactory.filter(), EditRegisterStates.waiting_street_selected],
        ),
    ]

    validation_message_list = [
        Handler(validation.not_valid_phone, [AdvancedRegisterStates.waiting_phone]),
        Handler(validation.not_valid_phone, [EditRegisterStates.waiting_phone]),
        Handler(validation.not_valid_street_name, [AdvancedRegisterStates.waiting_street_typing]),
        Handler(
            validation.not_valid_street_name,
            [AdvancedRegisterStates.waiting_street_selected, ~F.via_bot],
        ),
        Handler(validation.not_valid_street_name, [EditRegisterStates.waiting_street_typing]),
        Handler(
            validation.not_valid_street_name,
            [EditRegisterStates.waiting_street_selected, ~F.via_bot],
        ),
        Handler(validation.not_valid_flat, [AdvancedRegisterStates.waiting_flat]),
        Handler(validation.not_valid_flat, [EditRegisterStates.waiting_flat]),
        Handler(validation.not_valid_gender, [AdvancedRegisterStates.waiting_gender]),
        Handler(validation.not_valid_first_name, [AdvancedRegisterStates.waiting_first_name]),
        Handler(validation.not_valid_last_name, [AdvancedRegisterStates.waiting_middle_name]),
        Handler(validation.not_valid_middle_name, [AdvancedRegisterStates.waiting_last_name]),
        Handler(validation.not_valid_first_name, [EditRegisterStates.waiting_first_name]),
        Handler(validation.not_valid_last_name, [EditRegisterStates.waiting_middle_name]),
        Handler(validation.not_valid_middle_name, [EditRegisterStates.waiting_last_name]),
        Handler(validation.weak_password, [AdvancedRegisterStates.waiting_password]),
        Handler(validation.weak_password, [EditRegisterStates.waiting_password]),
        Handler(register.show_agreement, [AdvancedRegisterStates.waiting_agreement]),
    ]

    for message in [*register_message_list, *edit_message_list, *validation_message_list]:
        router.message.register(message.handler, *message.filters)

    for inline in inline_list:
        router.inline_query.register(inline.handler, *inline.filters)

    for callback in callback_list:
        router.callback_query.register(callback.handler, *callback.filters)

    return router
