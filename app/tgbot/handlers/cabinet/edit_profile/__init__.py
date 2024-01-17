from aiogram import Router, F

from filters.valid_name import ValidNameFilter
from handlers import validation
from handlers.cabinet.edit_profile import handlers
from keyboards.default.cabinet.edit_profile import edit_text
from keyboards.inline.callbacks import StreetCallbackFactory
from states.cabinet import EditInfo
from texts.keyboards import BACK


def prepare_router() -> Router():
    router = Router()

    router.message.register(
        handlers.confirm, EditInfo.waiting_acception, F.text == edit_text["accept_info_text"]
    )
    router.message.register(handlers.showing_user_info, F.text == BACK)
    router.message.register(
        handlers.handle_buttons, EditInfo.waiting_acception, F.text.in_(edit_text.values())
    )

    # Change names

    router.message.register(
        handlers.edit_first_name, EditInfo.waiting_first_name, ValidNameFilter()
    )
    router.message.register(
        handlers.edit_middle_name, EditInfo.waiting_middle_name, ValidNameFilter()
    )
    router.message.register(handlers.edit_last_name, EditInfo.waiting_last_name, ValidNameFilter())

    # Change street name

    router.message.register(handlers.edit_street, EditInfo.waiting_street_typing, F.text.len() >= 3)
    router.message.register(handlers.edit_street, EditInfo.waiting_street_selected, ~F.via_bot)

    router.inline_query.register(handlers.show_street_list, EditInfo.waiting_street_selected)
    router.callback_query.register(
        handlers.confirm_street, StreetCallbackFactory.filter(), EditInfo.waiting_street_selected
    )

    router.message.register(handlers.edit_house, EditInfo.waiting_house)
    router.message.register(handlers.edit_flat, EditInfo.waiting_flat, F.text.isdigit())

    router.message.register(handlers.edit_gender, EditInfo.waiting_gender)

    # Validations

    router.message.register(validation.not_valid_first_name, EditInfo.waiting_first_name)
    router.message.register(validation.not_valid_middle_name, EditInfo.waiting_middle_name)
    router.message.register(validation.not_valid_last_name, EditInfo.waiting_last_name)

    router.message.register(validation.not_valid_street_name, EditInfo.waiting_street_typing)
    router.message.register(validation.not_valid_flat, EditInfo.waiting_flat)

    return router
