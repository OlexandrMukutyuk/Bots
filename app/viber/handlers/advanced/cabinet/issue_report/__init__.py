from filters.back import BackFilter
from handlers import validation
from handlers.advanced.cabinet.issue_report import handlers
from handlers.common.helpers import full_cabinet_menu
from states import FullIssueReportStates
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.dispatcher.filters.builtin import StateFilter


def prepare_router(dp: Dispatcher):
    dp.text_messages_handler.subscribe(
        full_cabinet_menu, [StateFilter(FullIssueReportStates.waiting_issue_report), BackFilter()]
    )

    dp.text_messages_handler.subscribe(
        handlers.report_tech_issue,
        [
            StateFilter(FullIssueReportStates.waiting_issue_report),
            lambda r: len(r.message.text) >= 5,
        ],
    )
    dp.text_messages_handler.subscribe(
        validation.not_valid_text_with_back,
        [StateFilter(FullIssueReportStates.waiting_issue_report)],
    )
