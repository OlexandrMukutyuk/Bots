from dto.chat_bot import ReportIssueDto
from handlers.common.helpers import full_cabinet_menu
from services.http_client import HttpChatBot
from viber import viber
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.types import requests, messages


async def report_tech_issue(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    user_data = await state.get_data()

    await HttpChatBot.report_issue(
        ReportIssueDto(user_id=user_data.get("UserId"), comment=request.message.text)
    )

    await viber.send_message(
        request.sender.id,
        messages.TextMessage(text="Звернення відправлено успішно!"),
    )

    await full_cabinet_menu(request, data)
