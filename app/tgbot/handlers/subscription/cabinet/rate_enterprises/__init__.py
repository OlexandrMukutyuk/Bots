from aiogram import Router, F

from handlers.common.helpers import Handler
from handlers.subscription.cabinet.rate_enterprises import handlers
from keyboards.inline.callbacks import EnterpriseCallbackFactory, EnterpriseRateCallbackFactory
from states.subscription import RateEnterpriseStates


def prepare_router() -> Router:
    router = Router()

    callback_list = [
        # Showing list actions
        Handler(handlers.to_menu, [RateEnterpriseStates.showing_list, F.data == "back"]),
        Handler(
            handlers.show_rate_for_enterprises,
            [RateEnterpriseStates.showing_list, EnterpriseCallbackFactory.filter()],
        ),
        Handler(
            handlers.to_enterprise_list,
            [RateEnterpriseStates.enterprise_selected, F.data == "back"],
        ),
        Handler(
            handlers.rate_enterprise,
            [RateEnterpriseStates.enterprise_selected, EnterpriseRateCallbackFactory.filter()],
        ),
    ]

    for callback in callback_list:
        router.callback_query.register(callback.handler, *callback.filters)

    return router
