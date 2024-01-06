from aiogram import Router, F

from app.tgbot.handlers import validation
from app.tgbot.handlers.cabinet.issue_report import handlers
from app.tgbot.states.cabinet import IssueReportStates


def prepare_router() -> Router:
    router = Router()

    # Issue Report
    router.message.register(handlers.report_tech_issue, IssueReportStates.waiting_issue_report, F.text.len() > 5)

    router.message.register(validation.not_valid_text, IssueReportStates.waiting_issue_report)

    return router
