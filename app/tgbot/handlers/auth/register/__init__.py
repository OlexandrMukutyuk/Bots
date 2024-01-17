from aiogram import Router, F

from filters.strong_password import StrongPasswordFilter
from filters.valid_name import ValidNameFilter
from filters.valid_phone import ValidPhoneFilter
from handlers import validation
from handlers.auth.register import register, edit_info
from handlers.common.helpers import Handler
from handlers.common.streets import StreetsHandlers
from keyboards.default.auth.edit_info import edit_text
from keyboards.inline.callbacks import StreetCallbackFactory
from models import Gender
from states.advanced import RegisterState, EditRegisterState
from texts.keyboards import CHANGE_STREET, AGREEMENT, WITHOUT_FLAT


def prepare_router() -> Router:
    router = Router()

    register_message_list = [
        # Get phone
        Handler(register.save_phone, [RegisterState.waiting_phone, F.contact]),
        Handler(register.save_phone, [RegisterState.waiting_phone, ValidPhoneFilter()]),
        # Get street
        Handler(register.choose_street, [RegisterState.waiting_street_typing, F.text.len() >= 3]),
        Handler(
            StreetsHandlers.message_via_bot,
            [RegisterState.waiting_street_selected, F.via_bot],
        ),
        Handler(
            register.choose_street,
            [RegisterState.waiting_street_selected, F.text.len() >= 3, ~F.via_bot],
        ),
        # Change street
        Handler(register.change_street, [RegisterState.waiting_house, F.text == CHANGE_STREET]),
        # Get house
        Handler(register.save_house, [RegisterState.waiting_house]),
        # Get flat
        Handler(register.save_flat, [RegisterState.waiting_flat, F.text.isdigit()]),
        Handler(register.save_flat, [RegisterState.waiting_flat, F.text == WITHOUT_FLAT]),
        # Get first, middle, last Names
        Handler(register.save_first_name, [RegisterState.waiting_first_name, ValidNameFilter()]),
        Handler(
            register.save_middle_name,
            [RegisterState.waiting_middle_name, ValidNameFilter()],
        ),
        Handler(register.save_last_name, [RegisterState.waiting_last_name, ValidNameFilter()]),
        # Get gender
        Handler(
            register.save_gender,
            [RegisterState.waiting_gender, F.text.in_(Gender.values_reversed.keys())],
        ),
        # Get password & show agreement
        Handler(register.save_password, [RegisterState.waiting_password, StrongPasswordFilter()]),
        Handler(register.show_agreement, [RegisterState.waiting_password, F.text != AGREEMENT]),
    ]

    edit_message_list = [
        Handler(
            edit_info.first_time_showing_user_info,
            [RegisterState.waiting_agreement, F.text == AGREEMENT],
        ),
        # Showing typed info
        Handler(
            edit_info.handle_buttons,
            [EditRegisterState.waiting_accepting, F.text.in_(edit_text.values())],
        ),
        Handler(edit_info.first_time_showing_user_info, [EditRegisterState.waiting_accepting]),
        # Edit info
        Handler(
            edit_info.edit_first_name, [EditRegisterState.waiting_first_name, ValidNameFilter()]
        ),
        Handler(
            edit_info.edit_middle_name, [EditRegisterState.waiting_middle_name, ValidNameFilter()]
        ),
        Handler(edit_info.edit_last_name, [EditRegisterState.waiting_last_name, ValidNameFilter()]),
        Handler(edit_info.edit_phone, [EditRegisterState.waiting_phone, F.contact]),
        Handler(edit_info.edit_phone, [EditRegisterState.waiting_phone, ValidPhoneFilter()]),
        Handler(
            edit_info.edit_street, [EditRegisterState.waiting_street_typing, F.text.len() >= 3]
        ),
        Handler(
            edit_info.edit_street,
            [EditRegisterState.waiting_street_selected, F.text.len() >= 3, ~F.via_bot],
        ),
        Handler(
            StreetsHandlers.message_via_bot,
            [RegisterState.waiting_street_selected, F.via_bot],
        ),
        Handler(edit_info.edit_house, [EditRegisterState.waiting_house]),
        Handler(edit_info.edit_flat, [EditRegisterState.waiting_flat, F.text.isdigit()]),
        Handler(edit_info.edit_flat, [EditRegisterState.waiting_flat, F.text == WITHOUT_FLAT]),
        Handler(
            edit_info.edit_password, [EditRegisterState.waiting_password, StrongPasswordFilter()]
        ),
    ]

    inline_list = [
        Handler(register.show_street_list, [RegisterState.waiting_street_selected]),
        Handler(edit_info.show_street_list, [EditRegisterState.waiting_street_selected]),
    ]

    callback_list = [
        Handler(
            register.confirm_street,
            [StreetCallbackFactory.filter(), RegisterState.waiting_street_selected],
        ),
        Handler(
            edit_info.confirm_street,
            [StreetCallbackFactory.filter(), EditRegisterState.waiting_street_selected],
        ),
    ]

    validation_message_list = [
        Handler(validation.not_valid_phone, [RegisterState.waiting_phone]),
        Handler(validation.not_valid_phone, [EditRegisterState.waiting_phone]),
        Handler(validation.not_valid_street_name, [RegisterState.waiting_street_typing]),
        Handler(
            validation.not_valid_street_name,
            [RegisterState.waiting_street_selected, ~F.via_bot],
        ),
        Handler(validation.not_valid_street_name, [EditRegisterState.waiting_street_typing]),
        Handler(
            validation.not_valid_street_name,
            [EditRegisterState.waiting_street_selected, ~F.via_bot],
        ),
        Handler(validation.not_valid_flat, [RegisterState.waiting_flat]),
        Handler(validation.not_valid_flat, [EditRegisterState.waiting_flat]),
        Handler(validation.not_valid_gender, [RegisterState.waiting_gender]),
        Handler(validation.not_valid_first_name, [RegisterState.waiting_first_name]),
        Handler(validation.not_valid_last_name, [RegisterState.waiting_middle_name]),
        Handler(validation.not_valid_middle_name, [RegisterState.waiting_last_name]),
        Handler(validation.not_valid_first_name, [EditRegisterState.waiting_first_name]),
        Handler(validation.not_valid_last_name, [EditRegisterState.waiting_middle_name]),
        Handler(validation.not_valid_middle_name, [EditRegisterState.waiting_last_name]),
        Handler(validation.weak_password, [RegisterState.waiting_password]),
        Handler(validation.weak_password, [EditRegisterState.waiting_password]),
    ]

    for message in [*register_message_list, *edit_message_list, *validation_message_list]:
        router.message.register(message.handler, *message.filters)

    for inline in inline_list:
        router.inline_query.register(inline.handler, *inline.filters)

    for callback in callback_list:
        router.callback_query.register(callback.handler, *callback.filters)

    return router
