from aiogram import Router, F

from handlers.common.reference_info import ReferenceInfoHandlers
from handlers.guest.cabinet.menu import handlers as menu
from keyboards.inline.callbacks import ReferenceInfoCallbackFactory
from states.guest import ReferenceInfoStates


def prepare_router() -> Router:
    router = Router()

    router.callback_query.register(ReferenceInfoHandlers.show_info, ReferenceInfoStates.waiting_info, ReferenceInfoCallbackFactory.filter())
    router.callback_query.register(menu.to_main_menu_inline, ReferenceInfoStates.waiting_info, F.data == 'to_menu')

    return router
