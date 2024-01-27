from filters.back import BackFilter
from filters.no import NoFilter
from filters.valid_flat import ValidFlatFilter
from filters.yes import YesFilter
from handlers import validation
from handlers.advanced.cabinet.create_request import handlers
from handlers.advanced.cabinet.menu import handlers as menu
from handlers.common.helpers import Handler, full_cabinet_menu
from states import CreateRequestStates
from texts import (
    TO_MAIN_MENU,
    MANUALLY_ADDRESS,
    CHANGE_STREET,
    LIVING_IN_HOUSE,
    YES,
    NO,
    NO_NEED,
    ENOUGH,
)
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.dispatcher.filters.builtin import StateFilter


def prepare_router(dp: Dispatcher):
    message_list = [
        # To main cabinet
        Handler(
            full_cabinet_menu,
            [
                lambda r: r.message.text in [TO_MAIN_MENU, "to_menu"],
                StateFilter(CreateRequestStates),
            ],
        ),
        #
        # Choose problem
        Handler(
            full_cabinet_menu,
            [
                StateFilter(CreateRequestStates.waiting_problem),
                lambda r: r.message.text == "to_menu",
            ],
        ),
        Handler(
            handlers.confirm_problem,
            [StateFilter(CreateRequestStates.waiting_problem)],
        ),
        #
        # Choose reason
        Handler(
            menu.create_request,
            [
                StateFilter(CreateRequestStates.waiting_reason),
                lambda r: r.message.text == "back",
            ],
        ),
        Handler(
            handlers.confirm_reason,
            [StateFilter(CreateRequestStates.waiting_reason)],
        ),
        # Street choosing
        Handler(
            handlers.confirm_street,
            [StateFilter(CreateRequestStates.waiting_street_selected)],
        ),
        # Choose address
        Handler(
            handlers.flat_back, [StateFilter(CreateRequestStates.waiting_address), BackFilter()]
        ),
        Handler(
            handlers.request_on_my_site,
            [StateFilter(CreateRequestStates.waiting_address), YesFilter()],
        ),
        Handler(
            handlers.manually_type_location,
            [StateFilter(CreateRequestStates.waiting_address), NoFilter()],
        ),
        # Manually Address
        Handler(
            handlers.manually_address_back,
            [StateFilter(CreateRequestStates.is_address_manually), BackFilter()],
        ),
        # Street choosing
        Handler(
            handlers.ask_for_street_name,
            [
                StateFilter(CreateRequestStates.is_address_manually),
                lambda r: r.message.text == MANUALLY_ADDRESS,
            ],
        ),
        Handler(
            handlers.flat_back,
            [StateFilter(CreateRequestStates.waiting_street_typing), BackFilter()],
        ),
        Handler(
            handlers.type_street,
            [
                StateFilter(CreateRequestStates.waiting_street_typing),
                lambda r: len(r.message.text) >= 3,
            ],
        ),
        # Choose house
        Handler(
            handlers.ask_for_street_name,
            [
                StateFilter(CreateRequestStates.waiting_house),
                lambda r: r.message.text == CHANGE_STREET,
            ],
        ),
        Handler(handlers.save_house, [StateFilter(CreateRequestStates.waiting_house)]),
        # Choose flat
        Handler(handlers.flat_back, [StateFilter(CreateRequestStates.waiting_flat), BackFilter()]),
        Handler(
            handlers.save_flat, [StateFilter(CreateRequestStates.waiting_flat), ValidFlatFilter()]
        ),
        Handler(
            handlers.save_flat,
            [
                StateFilter(CreateRequestStates.waiting_flat),
                lambda r: r.message.text == LIVING_IN_HOUSE,
            ],
        ),
        # Choose comment
        Handler(
            handlers.ask_flat, [StateFilter(CreateRequestStates.waiting_comment), BackFilter()]
        ),
        Handler(
            handlers.save_comment,
            [
                StateFilter(CreateRequestStates.waiting_comment),
                lambda r: len(r.message.text) >= 10,
            ],
        ),
        # Choose showing on site
        Handler(
            handlers.showing_status_back,
            [StateFilter(CreateRequestStates.waiting_showing_status), BackFilter()],
        ),
        Handler(
            handlers.save_showing_status,
            [
                StateFilter(CreateRequestStates.waiting_showing_status),
                lambda r: r.message.text in [YES, NO],
            ],
        ),
        # Upload images
        Handler(
            handlers.saving_images_back,
            [StateFilter(CreateRequestStates.waiting_images), BackFilter()],
        ),
        Handler(
            handlers.saving_images,
            [
                StateFilter(CreateRequestStates.waiting_images),
                lambda r: r.message.text in [NO_NEED, ENOUGH],
            ],
        ),
        # Showing all info
        Handler(
            handlers.showing_request_info,
            [
                StateFilter(CreateRequestStates.waiting_confirm),
                lambda r: r.message.text not in [YES, NO],
            ],
        ),
        # Confirm request
        Handler(
            handlers.confirm_request,
            [StateFilter(CreateRequestStates.waiting_confirm), YesFilter()],
        ),
        Handler(
            handlers.reset_user_request_state,
            [StateFilter(CreateRequestStates.waiting_confirm), NoFilter()],
        ),
        # Validation handlers
        Handler(
            validation.not_valid_street_name,
            [StateFilter(CreateRequestStates.waiting_street_typing)],
        ),
        Handler(validation.not_valid_flat, [StateFilter(CreateRequestStates.waiting_flat)]),
        Handler(validation.not_valid_comment, [StateFilter(CreateRequestStates.waiting_comment)]),
        Handler(
            validation.not_valid_text, [StateFilter(CreateRequestStates.waiting_showing_status)]
        ),
    ]

    # Geo sharing
    dp.location_messages_handler.subscribe(
        handlers.location_by_geo, [StateFilter(CreateRequestStates.is_address_manually)]
    )
    # Photo uploading
    dp.picture_messages_handler.subscribe(
        handlers.saving_images, [StateFilter(CreateRequestStates.waiting_images)]
    )

    for message in message_list:
        dp.text_messages_handler.subscribe(message.handler, message.filters)
