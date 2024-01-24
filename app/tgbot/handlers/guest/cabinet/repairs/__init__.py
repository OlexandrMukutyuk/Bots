from aiogram import Router, F

from handlers import validation
from handlers.common.helpers import Handler
from handlers.guest.cabinet.menu import handlers as menu
from handlers.guest.cabinet.repairs import handlers
from keyboards.inline.callbacks import StreetCallbackFactory
from states.guest import RepairsStates
from texts import BACK


def prepare_router() -> Router:
    router = Router()

    callback_list = [
        Handler(handlers.my_address_repairs, [RepairsStates.waiting_address, F.data == 'repairs_my_address']),
        Handler(handlers.other_address_repairs, [RepairsStates.waiting_address, F.data == 'repairs_other_address']),
        Handler(menu.to_main_menu_inline, [RepairsStates.waiting_address, F.data == 'to_menu']),
        Handler(handlers.confirm_street, [StreetCallbackFactory.filter(), RepairsStates.waiting_street_selected])
    ]

    message_list = [
        Handler(menu.repairs, [RepairsStates.waiting_street_typing, F.text == BACK]),
        # Address
        Handler(handlers.type_street, [RepairsStates.waiting_street_typing, F.text.len() >= 3]),
        Handler(handlers.type_street, [RepairsStates.waiting_street_selected, F.text.len() >= 3, ~F.via_bot]),
        Handler(handlers.message_via_bot, [RepairsStates.waiting_street_selected, F.via_bot]),

        # Other
        Handler(handlers.save_house, [RepairsStates.waiting_house]),
        Handler(validation.not_valid_street_name, [RepairsStates.waiting_street_typing]),
        Handler(validation.not_valid_street_name, [RepairsStates.waiting_street_selected]),
    ]

    router.inline_query.register(
        handlers.show_inline_list, RepairsStates.waiting_street_selected
    )

    for message in message_list:
        router.message.register(message.handler, *message.filters)

    for callback in callback_list:
        router.callback_query.register(callback.handler, *callback.filters)

    return router
