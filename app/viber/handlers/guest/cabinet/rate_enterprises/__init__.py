from handlers.common.helpers import Handler
from handlers.guest.cabinet.rate_enterprises import handlers
from states import GuestRateEnterpriseStates
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.dispatcher.filters.builtin import StateFilter


def prepare_router(dp: Dispatcher):
    callback_list = [
        # Showing list actions
        Handler(
            handlers.to_menu,
            [
                StateFilter(GuestRateEnterpriseStates.showing_list),
                lambda r: r.message.text == "back",
            ],
        ),
        Handler(
            handlers.show_rate_for_enterprises,
            [StateFilter(GuestRateEnterpriseStates.showing_list)],
        ),
        Handler(
            handlers.to_enterprise_list,
            [
                StateFilter(GuestRateEnterpriseStates.enterprise_selected),
                lambda r: r.message.text == "back",
            ],
        ),
        Handler(
            handlers.rate_enterprise,
            [StateFilter(GuestRateEnterpriseStates.enterprise_selected)],
        ),
    ]

    for callback in callback_list:
        dp.text_messages_handler.subscribe(callback.handler, callback.filters)
