from handlers.advanced.cabinet.rate_enterprises import handlers
from handlers.common import helpers
from handlers.common.helpers import Handler
from states import FullRateEnterpriseStates
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.dispatcher.filters.builtin import StateFilter


def prepare_router(dp: Dispatcher):
    message_list = [
        # Showing list actions
        Handler(
            helpers.full_cabinet_menu,
            [
                StateFilter(FullRateEnterpriseStates.showing_list),
                lambda r: r.message.text == "back",
            ],
        ),
        Handler(
            handlers.show_rate_for_enterprises,
            [StateFilter(FullRateEnterpriseStates.showing_list)],
        ),
        Handler(
            handlers.to_enterprise_list,
            [
                StateFilter(FullRateEnterpriseStates.enterprise_selected),
                lambda r: r.message.text == "back",
            ],
        ),
        Handler(
            handlers.rate_enterprise,
            [StateFilter(FullRateEnterpriseStates.enterprise_selected)],
        ),
    ]

    for message in message_list:
        dp.text_messages_handler.subscribe(message.handler, message.filters)
