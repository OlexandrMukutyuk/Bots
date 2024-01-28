from handlers import validation
from handlers.advanced.cabinet.archive_req import handlers
from handlers.common.helpers import Handler, full_cabinet_menu
from states import ArchiveRequestsStates
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.dispatcher.filters.builtin import StateFilter


def prepare_router(dp: Dispatcher):
    message_list = [
        Handler(
            full_cabinet_menu,
            [
                StateFilter(ArchiveRequestsStates),
                lambda r: r.message.text == "to_menu",
            ],
        ),
        Handler(
            handlers.request_details,
            [
                StateFilter(ArchiveRequestsStates.waiting_req),
                lambda r: r.message.text.split(":")[0] == "DETAILS",
            ],
        ),
        Handler(
            handlers.review_request,
            [
                StateFilter(ArchiveRequestsStates.waiting_req),
                lambda r: r.message.text.split(":")[0] == "REVIEW",
            ],
        ),
        Handler(
            handlers.show_basic_info,
            [StateFilter(ArchiveRequestsStates.waiting_req)],
        ),
        Handler(handlers.save_rate, [StateFilter(ArchiveRequestsStates.waiting_rate)]),
        Handler(handlers.save_comment, [StateFilter(ArchiveRequestsStates.waiting_comment)]),
        # Validation
        Handler(validation.not_valid_text, [StateFilter(ArchiveRequestsStates.waiting_req)]),
        Handler(validation.not_valid_text, [StateFilter(ArchiveRequestsStates.waiting_comment)]),
    ]

    for message in message_list:
        dp.text_messages_handler.subscribe(message.handler, message.filters)
