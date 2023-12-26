from aiogram import Router, F
from aiogram.filters import Command

from filters.strong_password import StrongPasswordFilter
from filters.valid_name import ValidNameFilter
from filters.valid_phone import ValidPhoneFilter
from keyboards.default.auth.edit_info import edit_text
from keyboards.default.auth.register import change_street_text, without_flat_text, gender_dict, agreement_text
from keyboards.inline.callbacks import StreetCallbackFactory
from states.auth import AdvancedRegisterState, EditRegisterState
from . import edit_info
from . import register
from .. import validation


def prepare_router() -> Router:
    router = Router()

    # Get phone
    router.message.register(register.save_phone, AdvancedRegisterState.waiting_phone, F.contact)
    router.message.register(register.save_phone, AdvancedRegisterState.waiting_phone, ValidPhoneFilter())

    # Get street

    router.message.register(register.choose_street, AdvancedRegisterState.waiting_street_typing, F.text.len() >= 3)
    router.message.register(register.choose_street, AdvancedRegisterState.waiting_street_selected, F.text.len() >= 3,
                            ~F.via_bot)

    router.inline_query.register(register.show_street_list, AdvancedRegisterState.waiting_street_selected)
    router.callback_query.register(register.confirm_street, StreetCallbackFactory.filter(),
                                   AdvancedRegisterState.waiting_street_selected)

    # Change street
    router.message.register(register.change_street, AdvancedRegisterState.waiting_house, F.text == change_street_text)

    # Get house
    router.message.register(register.save_house, AdvancedRegisterState.waiting_house)

    # Get flat
    router.message.register(register.save_flat, AdvancedRegisterState.waiting_flat, F.text.isdigit())
    router.message.register(register.save_flat, AdvancedRegisterState.waiting_flat, F.text == without_flat_text)

    # Get first, middle, last Names

    router.message.register(register.save_first_name, AdvancedRegisterState.waiting_first_name, ValidNameFilter())
    router.message.register(register.save_middle_name, AdvancedRegisterState.waiting_middle_name, ValidNameFilter())
    router.message.register(register.save_last_name, AdvancedRegisterState.waiting_last_name, ValidNameFilter())

    # Get gender

    router.message.register(register.save_gender, AdvancedRegisterState.waiting_gender,
                            F.text.in_(gender_dict.values()))

    # Get password & show agreement

    router.message.register(register.save_password, AdvancedRegisterState.waiting_password, StrongPasswordFilter())
    router.message.register(register.show_agreement, AdvancedRegisterState.waiting_agreement, F.text != agreement_text)

    # Validation messages

    router.message.register(validation.not_valid_phone, AdvancedRegisterState.waiting_phone)

    router.message.register(validation.not_valid_street_name, AdvancedRegisterState.waiting_street_typing)
    router.message.register(validation.not_valid_street_name, AdvancedRegisterState.waiting_street_selected, ~F.via_bot)

    router.message.register(validation.not_valid_flat, AdvancedRegisterState.waiting_flat)
    router.message.register(validation.not_valid_gender, AdvancedRegisterState.waiting_gender)

    router.message.register(validation.not_valid_first_name, AdvancedRegisterState.waiting_first_name)
    router.message.register(validation.not_valid_middle_name, AdvancedRegisterState.waiting_middle_name)
    router.message.register(validation.not_valid_last_name, AdvancedRegisterState.waiting_last_name)

    router.message.register(validation.weak_password, AdvancedRegisterState.waiting_password)

    # Testing

    router.message.register(edit_info.fill_data, Command('fill'))

    # All done
    router.message.register(edit_info.accept_info, EditRegisterState.waiting_accepting,
                            F.text == edit_text['accept_info_text'])

    # Showing typed info

    router.message.register(edit_info.handle_buttons, EditRegisterState.waiting_accepting,
                            F.text.in_(edit_text.values()))

    router.message.register(edit_info.first_time_showing_user_info, EditRegisterState.waiting_accepting)

    router.message.register(edit_info.first_time_showing_user_info, AdvancedRegisterState.waiting_agreement,
                            F.text == agreement_text)
    router.message.register(edit_info.first_time_showing_user_info, EditRegisterState.waiting_accepting)

    # Edit info

    router.message.register(edit_info.edit_first_name, EditRegisterState.waiting_first_name, ValidNameFilter())
    router.message.register(edit_info.edit_middle_name, EditRegisterState.waiting_middle_name, ValidNameFilter())
    router.message.register(edit_info.edit_last_name, EditRegisterState.waiting_last_name, ValidNameFilter())

    router.message.register(edit_info.edit_phone, EditRegisterState.waiting_phone, F.contact)
    router.message.register(edit_info.edit_phone, EditRegisterState.waiting_phone, ValidPhoneFilter())

    router.message.register(edit_info.edit_street, EditRegisterState.waiting_street_typing, F.text.len() >= 3)
    router.message.register(edit_info.edit_street, EditRegisterState.waiting_street_selected, F.text.len() >= 3,
                            ~F.via_bot)

    router.inline_query.register(edit_info.show_street_list, EditRegisterState.waiting_street_selected)
    router.callback_query.register(edit_info.confirm_street, StreetCallbackFactory.filter(),
                                   EditRegisterState.waiting_street_selected)

    router.message.register(edit_info.edit_house, EditRegisterState.waiting_house)

    router.message.register(edit_info.edit_flat, EditRegisterState.waiting_flat, F.text.isdigit())
    router.message.register(edit_info.edit_flat, EditRegisterState.waiting_flat, F.text == without_flat_text)

    router.message.register(edit_info.edit_password, EditRegisterState.waiting_password, StrongPasswordFilter())

    return router
