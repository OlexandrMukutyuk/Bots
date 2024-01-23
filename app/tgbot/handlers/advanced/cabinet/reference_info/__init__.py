from aiogram import Router, F

from handlers.advanced.cabinet.common import back_to_menu
from handlers.common.reference_info import ReferenceInfoHandlers
from keyboards.inline.callbacks import ReferenceInfoCallbackFactory
from states.advanced import FullReferenceInfoStates


def prepare_router() -> Router:
    router = Router()

    router.callback_query.register(ReferenceInfoHandlers.show_info, FullReferenceInfoStates.waiting_info,
                                   ReferenceInfoCallbackFactory.filter())
    router.callback_query.register(back_to_menu, FullReferenceInfoStates.waiting_info, F.data == 'to_menu')

    return router
