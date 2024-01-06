from aiogram import Router, F

from app.tgbot.handlers.cabinet.rate_enterprises import handlers
from app.tgbot.keyboards.inline.callbacks import EnterpriseCallbackFactory, EnterpriseRateCallbackFactory
from app.tgbot.states.cabinet import RateEnterprise


def prepare_router() -> Router:
    router = Router()

    # Showing list actions
    router.callback_query.register(handlers.to_menu, RateEnterprise.showing_list, F.data == 'back')
    router.callback_query.register(handlers.show_rate_for_enterprises, RateEnterprise.showing_list,
                                   EnterpriseCallbackFactory.filter())

    # Showing rating actions

    router.callback_query.register(handlers.to_enterprise_list, RateEnterprise.enterprise_selected, F.data == 'back')
    router.callback_query.register(handlers.rate_enterprise, RateEnterprise.enterprise_selected,
                                   EnterpriseRateCallbackFactory.filter())

    return router
