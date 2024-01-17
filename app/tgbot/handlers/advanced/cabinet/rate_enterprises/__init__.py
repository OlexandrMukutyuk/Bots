from aiogram import Router, F

from handlers.advanced.cabinet.rate_enterprises import handlers
from keyboards.inline.callbacks import EnterpriseCallbackFactory, EnterpriseRateCallbackFactory
from states.advanced import FullRateEnterpriseStates


def prepare_router() -> Router:
    router = Router()

    # Showing list actions
    router.callback_query.register(
        handlers.to_menu, FullRateEnterpriseStates.showing_list, F.data == "back"
    )
    router.callback_query.register(
        handlers.show_rate_for_enterprises,
        FullRateEnterpriseStates.showing_list,
        EnterpriseCallbackFactory.filter(),
    )

    # Showing rating actions

    router.callback_query.register(
        handlers.to_enterprise_list, FullRateEnterpriseStates.enterprise_selected, F.data == "back"
    )
    router.callback_query.register(
        handlers.rate_enterprise,
        FullRateEnterpriseStates.enterprise_selected,
        EnterpriseRateCallbackFactory.filter(),
    )

    return router
