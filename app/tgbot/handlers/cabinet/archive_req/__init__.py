from aiogram import Router, F

from handlers import validation
from handlers.cabinet.archive_req import handlers
from handlers.common.helpers import Handler
from keyboards.default.cabinet.archive_req import later_text
from keyboards.inline.callbacks import ArchiveReqCallbackFactory
from states.cabinet import ArchiveRequests


def prepare_router() -> Router:
    router = Router()

    router.inline_query.register(handlers.archive_req_list, ArchiveRequests.waiting_req)

    callback_list = [
        Handler(
            handlers.back_to_main_menu,
            [ArchiveRequests.waiting_req, F.data == "cabinet_menu"],
        ),
        Handler(
            handlers.request_details,
            [ArchiveRequests.waiting_req, ArchiveReqCallbackFactory.filter(F.review == False)],
        ),
        Handler(
            handlers.review_request,
            [ArchiveRequests.waiting_req, ArchiveReqCallbackFactory.filter(F.review == True)],
        ),
    ]

    message_list = [
        Handler(handlers.delete_list_message, [ArchiveRequests.waiting_req, F.via_bot]),
        Handler(handlers.continue_later, [ArchiveRequests.waiting_rate, F.text == later_text]),
        Handler(handlers.save_rate, [ArchiveRequests.waiting_rate, F.text.contains("")]),
        Handler(handlers.save_comment, [ArchiveRequests.waiting_comment, F.text]),
        # Validation
        Handler(validation.not_valid_text, [ArchiveRequests.waiting_req]),
        Handler(validation.not_valid_text, [ArchiveRequests.waiting_comment]),
    ]

    for message in message_list:
        router.message.register(message.handler, *message.filters)

    for callback in callback_list:
        router.callback_query.register(callback.handler, *callback.filters)

    return router
