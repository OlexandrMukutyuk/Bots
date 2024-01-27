from handlers.advanced.cabinet import (
    menu,
    rate_enterprises,
    edit_info,
    reference_info,
    repairs,
    issue_report,
    create_request,
)
from viberio.dispatcher.dispatcher import Dispatcher


def prepare_router(dp: Dispatcher):
    menu.prepare_router(dp)
    rate_enterprises.prepare_router(dp)
    edit_info.prepare_router(dp)
    reference_info.prepare_router(dp)
    repairs.prepare_router(dp)
    issue_report.prepare_router(dp)
    create_request.prepare_router(dp)
