from handlers import validation
from handlers.advanced.cabinet.menu import handlers as menu
from handlers.advanced.cabinet.repairs import handlers
from handlers.common.helpers import Handler, full_cabinet_menu
from states import FullRepairsStates
from texts import BACK
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.dispatcher.filters.builtin import StateFilter


def prepare_router(dp: Dispatcher):
    message_list = [
        Handler(
            handlers.my_address_repairs,
            [
                StateFilter(FullRepairsStates.waiting_address),
                lambda r: r.message.text == "repairs_my_address",
            ],
        ),
        Handler(
            handlers.other_address_repairs,
            [
                StateFilter(FullRepairsStates.waiting_address),
                lambda r: r.message.text == "repairs_other_address",
            ],
        ),
        Handler(
            full_cabinet_menu,
            [StateFilter(FullRepairsStates.waiting_address), lambda r: r.message.text == "to_menu"],
        ),
        Handler(
            handlers.confirm_street,
            [StateFilter(FullRepairsStates.waiting_street_selected)],
        ),
        Handler(
            menu.repairs,
            [
                StateFilter(FullRepairsStates.waiting_street_typing),
                lambda r: r.message.text == BACK,
            ],
        ),
        # Address
        Handler(
            handlers.type_street,
            [
                StateFilter(FullRepairsStates.waiting_street_typing),
                lambda r: len(r.message.text) >= 3,
            ],
        ),
        # Other
        Handler(
            validation.not_valid_street_name, [StateFilter(FullRepairsStates.waiting_street_typing)]
        ),
        Handler(
            validation.not_valid_street_name,
            [StateFilter(FullRepairsStates.waiting_street_selected)],
        ),
    ]

    for message in message_list:
        dp.text_messages_handler.subscribe(message.handler, message.filters)
