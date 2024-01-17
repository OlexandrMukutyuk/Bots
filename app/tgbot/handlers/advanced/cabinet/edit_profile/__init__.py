from aiogram import Router, F
from aiogram.filters import StateFilter

from filters.valid_flat import ValidFlatFilter
from filters.valid_name import ValidNameFilter
from handlers import validation
from handlers.advanced.cabinet.edit_profile import handlers
from handlers.common.helpers import Handler
from keyboards.default.cabinet.edit_profile import edit_text
from keyboards.inline.callbacks import StreetCallbackFactory
from states.advanced import FullEditInfoStates
from texts.keyboards import BACK


def prepare_router() -> Router():
    router = Router()

    message_list = [
        Handler(
            handlers.confirm,
            [FullEditInfoStates.waiting_acceptation, F.text == edit_text["accept_info_text"]],
        ),
        Handler(handlers.showing_user_info, [StateFilter(FullEditInfoStates), F.text == BACK]),
        Handler(
            handlers.handle_buttons,
            [FullEditInfoStates.waiting_acceptation, F.text.in_(edit_text.values())],
        ),
        # Change names
        Handler(
            handlers.edit_first_name, [FullEditInfoStates.waiting_first_name, ValidNameFilter()]
        ),
        Handler(
            handlers.edit_middle_name, [FullEditInfoStates.waiting_middle_name, ValidNameFilter()]
        ),
        Handler(handlers.edit_last_name, [FullEditInfoStates.waiting_last_name, ValidNameFilter()]),
        # Change street name
        Handler(
            handlers.edit_street, [FullEditInfoStates.waiting_street_typing, F.text.len() >= 3]
        ),
        Handler(handlers.edit_street, [FullEditInfoStates.waiting_street_selected, ~F.via_bot]),
        # Other
        Handler(handlers.edit_house, [FullEditInfoStates.waiting_house]),
        Handler(handlers.edit_flat, [FullEditInfoStates.waiting_flat, ValidFlatFilter()]),
        Handler(handlers.edit_gender, [FullEditInfoStates.waiting_gender]),
    ]

    router.inline_query.register(
        handlers.show_street_list, FullEditInfoStates.waiting_street_selected
    )
    router.callback_query.register(
        handlers.confirm_street,
        StreetCallbackFactory.filter(),
        FullEditInfoStates.waiting_street_selected,
    )

    validation_list = [
        Handler(validation.not_valid_first_name, [FullEditInfoStates.waiting_first_name]),
        Handler(validation.not_valid_middle_name, [FullEditInfoStates.waiting_middle_name]),
        Handler(validation.not_valid_last_name, [FullEditInfoStates.waiting_last_name]),
        Handler(validation.not_valid_street_name, [FullEditInfoStates.waiting_street_typing]),
        Handler(validation.not_valid_flat, [FullEditInfoStates.waiting_flat]),
    ]

    for message in [*message_list, *validation_list]:
        router.message.register(message.handler, *message.filters)

    return router
