from filters.valid_flat import ValidFlatFilter
from filters.valid_name import ValidNameFilter
from handlers import validation
from handlers.advanced.cabinet.edit_info import handlers
from handlers.advanced.cabinet.menu import handlers as menu
from handlers.common.helpers import Handler
from keyboards.user import edit_text
from states.advanced import FullEditInfoStates
from texts.keyboards import BACK
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.dispatcher.filters.builtin import StateFilter


def prepare_router(dp: Dispatcher):
    message_list = [
        Handler(
            handlers.confirm,
            [
                StateFilter(FullEditInfoStates.waiting_acceptation),
                lambda r: r.message.text == edit_text["accept_info_text"],
            ],
        ),
        Handler(
            menu.send_edit_user_info,
            [StateFilter(FullEditInfoStates), lambda r: r.message.text == BACK],
        ),
        Handler(
            handlers.handle_buttons,
            [
                StateFilter(FullEditInfoStates.waiting_acceptation),
                lambda r: r.message.text in edit_text.values(),
            ],
        ),
        # Change names
        Handler(
            handlers.edit_first_name,
            [StateFilter(FullEditInfoStates.waiting_first_name), ValidNameFilter()],
        ),
        Handler(
            handlers.edit_middle_name,
            [StateFilter(FullEditInfoStates.waiting_middle_name), ValidNameFilter()],
        ),
        Handler(
            handlers.edit_last_name,
            [StateFilter(FullEditInfoStates.waiting_last_name), ValidNameFilter()],
        ),
        # Change street name
        Handler(
            handlers.edit_street,
            [
                StateFilter(FullEditInfoStates.waiting_street_typing),
                lambda r: len(r.message.text) >= 3,
            ],
        ),
        Handler(
            handlers.confirm_street,
            [StateFilter(FullEditInfoStates.waiting_street_selected)],
        ),
        # Other
        Handler(handlers.edit_house, [StateFilter(FullEditInfoStates.waiting_house)]),
        Handler(
            handlers.edit_flat, [StateFilter(FullEditInfoStates.waiting_flat), ValidFlatFilter()]
        ),
        Handler(handlers.edit_gender, [StateFilter(FullEditInfoStates.waiting_gender)]),
    ]

    validation_list = [
        Handler(
            validation.not_valid_first_name, [StateFilter(FullEditInfoStates.waiting_first_name)]
        ),
        Handler(
            validation.not_valid_middle_name, [StateFilter(FullEditInfoStates.waiting_middle_name)]
        ),
        Handler(
            validation.not_valid_last_name, [StateFilter(FullEditInfoStates.waiting_last_name)]
        ),
        Handler(
            validation.not_valid_street_name,
            [StateFilter(FullEditInfoStates.waiting_street_typing)],
        ),
        Handler(validation.not_valid_edit_flat, [StateFilter(FullEditInfoStates.waiting_flat)]),
    ]

    for message in [*message_list, *validation_list]:
        dp.text_messages_handler.subscribe(message.handler, message.filters)
