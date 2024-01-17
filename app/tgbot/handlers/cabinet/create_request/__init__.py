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
from states.cabinet import CreateRequest
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
        Handler(handlers.message_via_bot, [CreateRequest.waiting_problem, F.via_bot]),
        Handler(handlers.message_via_bot, [CreateRequest.waiting_reason, F.via_bot]),
        # Choose address
        Handler(handlers.flat_back, [CreateRequest.waiting_address, BackFilter()]),
        Handler(handlers.request_on_my_site, [CreateRequest.waiting_address, YesFilter()]),
        Handler(handlers.manually_type_location, [CreateRequest.waiting_address, NoFilter()]),
        # Manually Address
        Handler(handlers.manually_address_back, [CreateRequest.is_address_manually, BackFilter()]),
        # Geo sharing
        Handler(handlers.location_by_geo, [CreateRequest.is_address_manually, F.location]),
        # Street choosing
        Handler(
            handlers.ask_for_street_name,
            [CreateRequest.is_address_manually, F.text == MANUALLY_ADDRESS],
        ),
        Handler(handlers.choose_street, [CreateRequest.waiting_street_typing, F.text.len() >= 3]),
        Handler(
            StreetsHandlers.message_via_bot, [CreateRequest.waiting_street_selected, F.via_bot]
        ),
        # Choose house
        Handler(
            handlers.ask_for_street_name,
            [CreateRequest.waiting_house, F.text == CHANGE_STREET],
        ),
        Handler(handlers.save_house, [CreateRequest.waiting_house]),
        # Choose flat
        Handler(handlers.flat_back, [CreateRequest.waiting_flat, BackFilter()]),
        Handler(handlers.save_flat, [CreateRequest.waiting_flat, F.text.isdigit()]),
        Handler(handlers.save_flat, [CreateRequest.waiting_flat, F.text == LIVING_IN_HOUSE]),
        # Choose comment
        Handler(handlers.comment_back, [CreateRequest.waiting_comment, BackFilter()]),
        Handler(handlers.save_comment, [CreateRequest.waiting_comment, F.text.len() >= 10]),
        # Choose showing on site
        Handler(handlers.showing_status_back, [CreateRequest.waiting_showing_status, BackFilter()]),
        Handler(
            handlers.save_showing_status,
            [CreateRequest.waiting_showing_status, F.text.in_([yes_text, no_text])],
        ),
        # Upload images
        Handler(handlers.saving_images_back, [CreateRequest.waiting_images, BackFilter()]),
        Handler(handlers.saving_images, [CreateRequest.waiting_images, F.photo]),
        Handler(
            handlers.saving_images,
            [CreateRequest.waiting_images, F.text.in_([NO_NEED, ENOUGH])],
        ),
        # Showing all info
        Handler(
            handlers.showing_request_info,
            [CreateRequest.waiting_confirm, ~F.text.in_([yes_text, no_text])],
        ),
        # Confirm request
        Handler(handlers.confirm_request, [CreateRequest.waiting_confirm, YesFilter()]),
        Handler(handlers.to_main_menu_inline, [CreateRequest.waiting_confirm, NoFilter()]),
        # Validation handlers
        Handler(validation.not_valid_flat, [CreateRequest.waiting_flat]),
        Handler(validation.not_valid_comment, [CreateRequest.waiting_comment]),
        Handler(validation.not_valid_text, [CreateRequest.waiting_showing_status]),
    ]

    inline_list = [
        # Choose problem
        Handler(handlers.show_problems_list, [CreateRequest.waiting_problem]),
        # Choose reason
        Handler(handlers.show_reasons_list, [CreateRequest.waiting_reason]),
        # Street choosing
        Handler(handlers.show_street_list, [CreateRequest.waiting_street_selected]),
    ]

    callback_list = [
        # To main cabinet
        Handler(handlers.to_main_menu_inline, [F.text == TO_MAIN_MENU]),
        # Choose problem
        Handler(
            handlers.confirm_problem,
            [ProblemCallbackFactory.filter(), CreateRequest.waiting_problem],
        ),
        Handler(handlers.cancel_problem, [CreateRequest.waiting_problem, F.data == "cabinet_menu"]),
        # Choose reason
        Handler(
            handlers.confirm_reason, [ProblemCallbackFactory.filter(), CreateRequest.waiting_reason]
        ),
        Handler(handlers.cancel_reason, [CreateRequest.waiting_reason, F.data == "back"]),
        # Street choosing
        Handler(
            handlers.confirm_street,
            [StreetCallbackFactory.filter(), CreateRequest.waiting_street_selected],
        ),
    ]

    for message in message_list:
        router.message.register(message.handler, *message.filters)

    for inline in inline_list:
        router.inline_query.register(inline.handler, *inline.filters)

    for callback in callback_list:
        router.callback_query.register(callback.handler, *callback.filters)

    return router
