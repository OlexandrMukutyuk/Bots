from aiogram import Router, F

from handlers import validation
from handlers.cabinet.archive_req import handlers
from keyboards.default.cabinet.archive_req import later_text
from keyboards.inline.callbacks import ArchiveReqCallbackFactory
from states.cabinet import ArchiveRequests


def prepare_router() -> Router:
    router = Router()

    router.inline_query.register(handlers.archive_req_list, ArchiveRequests.waiting_req)

    router.callback_query.register(handlers.back_to_main_menu, ArchiveRequests.waiting_req, F.data == 'cabinet_menu')
    router.message.register(handlers.delete_list_message, ArchiveRequests.waiting_req, F.via_bot)

    router.callback_query.register(handlers.handdle_archive_req, ArchiveRequests.waiting_req,
                                   ArchiveReqCallbackFactory.filter())

    router.message.register(handlers.continue_later, ArchiveRequests.waiting_rate, F.text == later_text)
    router.message.register(handlers.save_rate, ArchiveRequests.waiting_rate, F.text.contains(''))
    router.message.register(handlers.save_comment, ArchiveRequests.waiting_comment, F.text)

    # Validation

    router.message.register(validation.not_valid_text, ArchiveRequests.waiting_req)
    router.message.register(validation.not_valid_text, ArchiveRequests.waiting_comment)

    return router
