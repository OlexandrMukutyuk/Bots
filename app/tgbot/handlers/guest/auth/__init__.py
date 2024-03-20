from aiogram import Router, F
from handlers.common.city import CityHandlers
from handlers.common.helpers import Handler
from handlers.common.streets import StreetsHandlers
from handlers.guest.auth import handlers
from keyboards.inline.callbacks import StreetCallbackFactory
from states.guest import GuestAuthStates
from texts.keyboards import CHANGE_STREET

from handlers import validation


def prepare_router() -> Router:
    router = Router()

    message_list = [
        Handler(handlers.choice_region, [GuestAuthStates.waiting_choice_region, F.text.len() >= 3]),
        Handler(
            handlers.choose_city,
            [GuestAuthStates.waiting_city_typing, F.text.len() >= 3],
        ),
        Handler(
            CityHandlers.message_via_bot,
            [GuestAuthStates.waiting_city_selected, F.via_bot],
        ),
        Handler(
            handlers.choose_city,
            [GuestAuthStates.waiting_city_selected, F.text.len() >= 3, ~F.via_bot],
        ),

        Handler(handlers.type_street, [GuestAuthStates.waiting_street_typing, F.text.len() >= 3]),
        Handler(
            handlers.type_street,
            [GuestAuthStates.waiting_street_selected, ~F.via_bot, F.text.len() >= 3],
        ),
        Handler(
            handlers.choose_other_location,
            [GuestAuthStates.waiting_other_location, F.text.len() >= 3],
        ),
        Handler(
            StreetsHandlers.message_via_bot,
            [GuestAuthStates.waiting_street_selected, F.via_bot],
        ),
        Handler(handlers.change_street, [GuestAuthStates.waiting_house, F.text == CHANGE_STREET]),
        Handler(handlers.save_house, [GuestAuthStates.waiting_house]),
        # Validation
        Handler(validation.not_valid_street_name, [GuestAuthStates.waiting_street_typing]),
        Handler(validation.not_valid_street_name, [GuestAuthStates.waiting_street_selected]),
        Handler(validation.not_valid_street_name, [GuestAuthStates.waiting_city_typing]),
        Handler(validation.not_valid_street_name, [GuestAuthStates.waiting_city_selected]),
    ]

    router.inline_query.register(handlers.inline_list, GuestAuthStates.waiting_street_selected)
    router.inline_query.register(handlers.show_city_list, GuestAuthStates.waiting_city_selected)
    router.callback_query.register(
        handlers.choose_other_location,
        StreetCallbackFactory.filter(),
        GuestAuthStates.waiting_other_location,
    )
    router.callback_query.register(
        handlers.confirm_street,
        StreetCallbackFactory.filter(),
        GuestAuthStates.waiting_street_selected,
    )
    router.callback_query.register(
        handlers.confirm_city,
        StreetCallbackFactory.filter(),
        GuestAuthStates.waiting_city_selected,
    )

    for message in message_list:
        router.message.register(message.handler, *message.filters)

    return router
