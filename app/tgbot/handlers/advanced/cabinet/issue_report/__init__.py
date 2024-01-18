from aiogram import Router, F

from handlers import validation
from handlers.advanced.cabinet.issue_report import handlers
from states.advanced import FullIssueReportStates


def prepare_router() -> Router:
    router = Router()

    # Issue Report
    router.message.register(
        handlers.report_tech_issue, FullIssueReportStates.waiting_issue_report, F.text.len() > 5
    )

    router.message.register(
        validation.not_valid_text_with_back, FullIssueReportStates.waiting_issue_report
    )

    return router
