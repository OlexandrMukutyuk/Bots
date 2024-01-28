from aiogram import Router, F

from handlers import validation
from handlers.advanced.cabinet.archive_req import handlers
from handlers.common.helpers import Handler
from keyboards.default.cabinet.archive_req import later_text
from keyboards.inline.callbacks import ArchiveReqCallbackFactory
from states.advanced import ArchiveRequestsStates


def prepare_router() -> Router:
    router = Router()

    router.inline_query.register(handlers.archive_req_list, ArchiveRequestsStates.waiting_req)

    callback_list = [
        Handler(
            handlers.back_to_main_menu,
            [ArchiveRequestsStates.waiting_req, F.data == "cabinet_menu"],
        ),
        Handler(
            handlers.request_details,
            [
                ArchiveRequestsStates.waiting_req,
                ArchiveReqCallbackFactory.filter(F.review == False),
            ],
        ),
        Handler(
            handlers.review_request,
            [ArchiveRequestsStates.waiting_req, ArchiveReqCallbackFactory.filter(F.review == True)],
        ),
    ]

    message_list = [
        Handler(handlers.delete_list_message, [ArchiveRequestsStates.waiting_req, F.via_bot]),
        Handler(
            handlers.continue_later, [ArchiveRequestsStates.waiting_rate, F.text == later_text]
        ),
        Handler(handlers.save_rate, [ArchiveRequestsStates.waiting_rate, F.text.contains("")]),
        Handler(handlers.save_comment, [ArchiveRequestsStates.waiting_comment, F.text]),
        # Validation
        Handler(validation.not_valid_text, [ArchiveRequestsStates.waiting_req]),
        Handler(validation.not_valid_text, [ArchiveRequestsStates.waiting_comment]),

        #
    ]

    for message in message_list:
        router.message.register(message.handler, *message.filters)

    for callback in callback_list:
        router.callback_query.register(callback.handler, *callback.filters)

    return router
