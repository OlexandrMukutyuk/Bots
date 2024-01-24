from aiogram import Router, F

from handlers import validation
from handlers.advanced.cabinet.menu import handlers as menu
from handlers.advanced.cabinet.repairs import handlers
from handlers.common.helpers import Handler
from keyboards.inline.callbacks import StreetCallbackFactory
from states.advanced import FullRepairsStates
from texts import BACK


def prepare_router() -> Router:
    router = Router()

    callback_list = [
        Handler(handlers.my_address_repairs, [FullRepairsStates.waiting_address, F.data == 'repairs_my_address']),
        Handler(handlers.other_address_repairs, [FullRepairsStates.waiting_address, F.data == 'repairs_other_address']),
        Handler(menu.to_main_menu_inline, [FullRepairsStates.waiting_address, F.data == 'to_menu']),
        Handler(handlers.confirm_street, [StreetCallbackFactory.filter(), FullRepairsStates.waiting_street_selected])
    ]

    message_list = [
        Handler(menu.repairs, [FullRepairsStates.waiting_street_typing, F.text == BACK]),
        # Address
        Handler(handlers.type_street, [FullRepairsStates.waiting_street_typing, F.text.len() >= 3]),
        Handler(handlers.type_street, [FullRepairsStates.waiting_street_selected, F.text.len() >= 3, ~F.via_bot]),
        Handler(handlers.message_via_bot, [FullRepairsStates.waiting_street_selected, F.via_bot]),

        # Other
        Handler(validation.not_valid_street_name, [FullRepairsStates.waiting_street_typing]),
        Handler(validation.not_valid_street_name, [FullRepairsStates.waiting_street_selected]),
    ]

    router.inline_query.register(
        handlers.show_inline_list, FullRepairsStates.waiting_street_selected
    )

    for message in message_list:
        router.message.register(message.handler, *message.filters)

    for callback in callback_list:
        router.callback_query.register(callback.handler, *callback.filters)

    return router
