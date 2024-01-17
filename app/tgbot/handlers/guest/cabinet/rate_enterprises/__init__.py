from aiogram import Router, F

from handlers.common.helpers import Handler
from handlers.guest.cabinet.rate_enterprises import handlers
from keyboards.inline.callbacks import EnterpriseCallbackFactory, EnterpriseRateCallbackFactory
from states.guest import GuestRateEnterpriseStates


def prepare_router() -> Router:
    router = Router()

    callback_list = [
        # Showing list actions
        Handler(handlers.to_menu, [GuestRateEnterpriseStates.showing_list, F.data == "back"]),
        Handler(
            handlers.show_rate_for_enterprises,
            [GuestRateEnterpriseStates.showing_list, EnterpriseCallbackFactory.filter()],
        ),
        Handler(
            handlers.to_enterprise_list,
            [GuestRateEnterpriseStates.enterprise_selected, F.data == "back"],
        ),
        Handler(
            handlers.rate_enterprise,
            [GuestRateEnterpriseStates.enterprise_selected, EnterpriseRateCallbackFactory.filter()],
        ),
    ]

    for callback in callback_list:
        router.callback_query.register(callback.handler, *callback.filters)

    return router
