from aiogram import Router, F

from handlers.common.reference_info import ReferenceInfoHandlers
from handlers.guest.cabinet.reference_info.handlers import exit_ref_info
from keyboards.inline.callbacks import ReferenceInfoCallbackFactory
from states.guest import ReferenceInfoStates


def prepare_router() -> Router:
    router = Router()

    router.callback_query.register(ReferenceInfoHandlers.show_info, ReferenceInfoStates.waiting_info,
                                   ReferenceInfoCallbackFactory.filter())
    router.callback_query.register(exit_ref_info, ReferenceInfoStates.waiting_info, F.data == 'to_menu')

    return router
