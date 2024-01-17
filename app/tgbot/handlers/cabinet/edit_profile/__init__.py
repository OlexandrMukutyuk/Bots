from aiogram import Router, F

from filters.valid_name import ValidNameFilter
from handlers import validation
from handlers.cabinet.edit_profile import handlers
from keyboards.default.cabinet.edit_profile import edit_text
from keyboards.inline.callbacks import StreetCallbackFactory
from states.advanced import EditInfoStates
from texts.keyboards import BACK


def prepare_router() -> Router():
    router = Router()

    router.message.register(
        handlers.confirm,
        EditInfoStates.waiting_acceptation,
        F.text == edit_text["accept_info_text"],
    )
    router.message.register(handlers.showing_user_info, F.text == BACK)
    router.message.register(
        handlers.handle_buttons, EditInfoStates.waiting_acceptation, F.text.in_(edit_text.values())
    )

    # Change names

    router.message.register(
        handlers.edit_first_name, EditInfoStates.waiting_first_name, ValidNameFilter()
    )
    router.message.register(
        handlers.edit_middle_name, EditInfoStates.waiting_middle_name, ValidNameFilter()
    )
    router.message.register(
        handlers.edit_last_name, EditInfoStates.waiting_last_name, ValidNameFilter()
    )

    # Change street name

    router.message.register(
        handlers.edit_street, EditInfoStates.waiting_street_typing, F.text.len() >= 3
    )
    router.message.register(
        handlers.edit_street, EditInfoStates.waiting_street_selected, ~F.via_bot
    )

    router.inline_query.register(handlers.show_street_list, EditInfoStates.waiting_street_selected)
    router.callback_query.register(
        handlers.confirm_street,
        StreetCallbackFactory.filter(),
        EditInfoStates.waiting_street_selected,
    )

    router.message.register(handlers.edit_house, EditInfoStates.waiting_house)
    router.message.register(handlers.edit_flat, EditInfoStates.waiting_flat, F.text.isdigit())

    router.message.register(handlers.edit_gender, EditInfoStates.waiting_gender)

    # Validations

    router.message.register(validation.not_valid_first_name, EditInfoStates.waiting_first_name)
    router.message.register(validation.not_valid_middle_name, EditInfoStates.waiting_middle_name)
    router.message.register(validation.not_valid_last_name, EditInfoStates.waiting_last_name)

    router.message.register(validation.not_valid_street_name, EditInfoStates.waiting_street_typing)
    router.message.register(validation.not_valid_flat, EditInfoStates.waiting_flat)

    return router
