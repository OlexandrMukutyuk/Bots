from aiogram import Router, F

from filters.back import BackFilter
from filters.no import NoFilter
from filters.yes import YesFilter
from handlers import validation
from handlers.cabinet.create_request import handlers
from handlers.cabinet.create_request import handlers
from handlers.common.helpers import Handler
from handlers.common.streets import StreetsHandlers
from keyboards.default.start import yes_text, no_text
from keyboards.inline.callbacks import ProblemCallbackFactory, StreetCallbackFactory
from states.advanced import CreateRequestStates
from texts.keyboards import (
    TO_MAIN_MENU,
    MANUALLY_ADDRESS,
    CHANGE_STREET,
    LIVING_IN_HOUSE,
    NO_NEED,
    ENOUGH,
)


def prepare_router() -> Router:
    router = Router()

    message_list = [
        # To main cabinet
        Handler(handlers.to_main_menu_reply, [F.text == TO_MAIN_MENU]),
        # Choose problem
        Handler(handlers.message_via_bot, [CreateRequestStates.waiting_problem, F.via_bot]),
        Handler(handlers.message_via_bot, [CreateRequestStates.waiting_reason, F.via_bot]),
        # Choose address
        Handler(handlers.flat_back, [CreateRequestStates.waiting_address, BackFilter()]),
        Handler(handlers.request_on_my_site, [CreateRequestStates.waiting_address, YesFilter()]),
        Handler(handlers.manually_type_location, [CreateRequestStates.waiting_address, NoFilter()]),
        # Manually Address
        Handler(
            handlers.manually_address_back, [CreateRequestStates.is_address_manually, BackFilter()]
        ),
        # Geo sharing
        Handler(handlers.location_by_geo, [CreateRequestStates.is_address_manually, F.location]),
        # Street choosing
        Handler(
            handlers.ask_for_street_name,
            [CreateRequestStates.is_address_manually, F.text == MANUALLY_ADDRESS],
        ),
        Handler(
            handlers.choose_street, [CreateRequestStates.waiting_street_typing, F.text.len() >= 3]
        ),
        Handler(
            StreetsHandlers.message_via_bot,
            [CreateRequestStates.waiting_street_selected, F.via_bot],
        ),
        # Choose house
        Handler(
            handlers.ask_for_street_name,
            [CreateRequestStates.waiting_house, F.text == CHANGE_STREET],
        ),
        Handler(handlers.save_house, [CreateRequestStates.waiting_house]),
        # Choose flat
        Handler(handlers.flat_back, [CreateRequestStates.waiting_flat, BackFilter()]),
        Handler(handlers.save_flat, [CreateRequestStates.waiting_flat, F.text.isdigit()]),
        Handler(handlers.save_flat, [CreateRequestStates.waiting_flat, F.text == LIVING_IN_HOUSE]),
        # Choose comment
        Handler(handlers.comment_back, [CreateRequestStates.waiting_comment, BackFilter()]),
        Handler(handlers.save_comment, [CreateRequestStates.waiting_comment, F.text.len() >= 10]),
        # Choose showing on site
        Handler(
            handlers.showing_status_back, [CreateRequestStates.waiting_showing_status, BackFilter()]
        ),
        Handler(
            handlers.save_showing_status,
            [CreateRequestStates.waiting_showing_status, F.text.in_([yes_text, no_text])],
        ),
        # Upload images
        Handler(handlers.saving_images_back, [CreateRequestStates.waiting_images, BackFilter()]),
        Handler(handlers.saving_images, [CreateRequestStates.waiting_images, F.photo]),
        Handler(
            handlers.saving_images,
            [CreateRequestStates.waiting_images, F.text.in_([NO_NEED, ENOUGH])],
        ),
        # Showing all info
        Handler(
            handlers.showing_request_info,
            [CreateRequestStates.waiting_confirm, ~F.text.in_([yes_text, no_text])],
        ),
        # Confirm request
        Handler(handlers.confirm_request, [CreateRequestStates.waiting_confirm, YesFilter()]),
        Handler(handlers.to_main_menu_inline, [CreateRequestStates.waiting_confirm, NoFilter()]),
        # Validation handlers
        Handler(validation.not_valid_flat, [CreateRequestStates.waiting_flat]),
        Handler(validation.not_valid_comment, [CreateRequestStates.waiting_comment]),
        Handler(validation.not_valid_text, [CreateRequestStates.waiting_showing_status]),
    ]

    inline_list = [
        # Choose problem
        Handler(handlers.show_problems_list, [CreateRequestStates.waiting_problem]),
        # Choose reason
        Handler(handlers.show_reasons_list, [CreateRequestStates.waiting_reason]),
        # Street choosing
        Handler(handlers.show_street_list, [CreateRequestStates.waiting_street_selected]),
    ]

    callback_list = [
        # To main cabinet
        Handler(handlers.to_main_menu_inline, [F.text == TO_MAIN_MENU]),
        # Choose problem
        Handler(
            handlers.confirm_problem,
            [ProblemCallbackFactory.filter(), CreateRequestStates.waiting_problem],
        ),
        Handler(
            handlers.cancel_problem, [CreateRequestStates.waiting_problem, F.data == "cabinet_menu"]
        ),
        # Choose reason
        Handler(
            handlers.confirm_reason,
            [ProblemCallbackFactory.filter(), CreateRequestStates.waiting_reason],
        ),
        Handler(handlers.cancel_reason, [CreateRequestStates.waiting_reason, F.data == "back"]),
        # Street choosing
        Handler(
            handlers.confirm_street,
            [StreetCallbackFactory.filter(), CreateRequestStates.waiting_street_selected],
        ),
    ]

    for message in message_list:
        router.message.register(message.handler, *message.filters)

    for inline in inline_list:
        router.inline_query.register(inline.handler, *inline.filters)

    for callback in callback_list:
        router.callback_query.register(callback.handler, *callback.filters)

    return router
