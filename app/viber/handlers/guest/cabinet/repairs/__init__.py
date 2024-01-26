from handlers import validation
from handlers.common.helpers import Handler
from handlers.guest.cabinet.menu import handlers as menu
from handlers.guest.cabinet.repairs import handlers
from states import RepairsStates
from texts import BACK
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.dispatcher.filters.builtin import StateFilter


def prepare_router(dp: Dispatcher):
    message_list = [
        Handler(
            handlers.my_address_repairs,
            [
                StateFilter(RepairsStates.waiting_address),
                lambda r: r.message.text == "repairs_my_address",
            ],
        ),
        Handler(
            handlers.other_address_repairs,
            [
                StateFilter(RepairsStates.waiting_address),
                lambda r: r.message.text == "repairs_other_address",
            ],
        ),
        Handler(
            menu.show_cabinet_menu,
            [StateFilter(RepairsStates.waiting_address), lambda r: r.message.text == "to_menu"],
        ),
        Handler(handlers.confirm_street, [StateFilter(RepairsStates.waiting_street_selected)]),
        Handler(
            menu.repairs,
            [StateFilter(RepairsStates.waiting_street_typing), lambda r: r.message.text == BACK],
        ),
        # Address
        Handler(
            handlers.type_street,
            [StateFilter(RepairsStates.waiting_street_typing), lambda r: len(r.message.text) >= 3],
        ),
        Handler(
            handlers.type_street,
            [
                StateFilter(RepairsStates.waiting_street_selected),
                lambda r: len(r.message.text) >= 3,
            ],
        ),
        # Other
        Handler(handlers.save_house, [StateFilter(RepairsStates.waiting_house)]),
        Handler(
            validation.not_valid_street_name, [StateFilter(RepairsStates.waiting_street_typing)]
        ),
        Handler(
            validation.not_valid_street_name, [StateFilter(RepairsStates.waiting_street_selected)]
        ),
    ]

    for message in message_list:
        dp.text_messages_handler.subscribe(message.handler, message.filters)
