from handlers.common.email import EmailHandlers
from handlers.start.handlers import asking_email
from states import LoginState
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.types import requests


async def check_email_code(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    async def action():
        return await asking_email(request, data)

    await EmailHandlers.check_code(
        request=request,
        state=state,
        failure_state=LoginState.waiting_code,
        other_email_action=action,
    )
