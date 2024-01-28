import texts
from dto.chat_bot import UserIdDto
from handlers.common.enterprises import EnterprisesHandlers
from handlers.common.helpers import full_cabinet_menu
from handlers.common.reference_info import ReferenceInfoHandlers
from keyboards.archive_requests import generate_archive_req_kb
from keyboards.cabinet import cabinet_menu_text
from keyboards.common import back_kb
from keyboards.create_request import generate_problem_kb
from keyboards.repairs import repairs_kb
from keyboards.user import edit_profile_kb
from models import Gender
from services.database import update_last_message
from services.http_client import HttpChatBot
from states import (
    FullRateEnterpriseStates,
    FullEditInfoStates,
    FullReferenceInfoStates,
    FullRepairsStates,
    FullIssueReportStates,
    CreateRequestStates,
    ArchiveRequestsStates,
)
from utils.template_engine import render_template
from viber import viber
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.types import requests, messages


async def main_handler(request: requests.ViberMessageRequest, data: dict):
    button_text = request.message.text

    if button_text == cabinet_menu_text["create_request"]:
        return await create_request(request, data)

    if button_text == cabinet_menu_text["actual_requests"]:
        return await actual_requests(request, data)

    if button_text == cabinet_menu_text["report_issue"]:
        return await report_issue(request, data)

    if button_text == cabinet_menu_text["review_enterprises"]:
        return await rate_enterprises(request, data)

    if button_text == cabinet_menu_text["history_requests"]:
        return await history_requests(request, data)

    if button_text == cabinet_menu_text["change_user_info"]:
        return await send_edit_user_info(request, data)

    if button_text == cabinet_menu_text["reference_info"]:
        return await reference_info(request, data)

    if button_text == cabinet_menu_text["repairs"]:
        return await repairs(request, data)


async def repairs(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    sender_id = request.sender.id
    await update_last_message(sender_id, texts.ASKING_REPAIRS, repairs_kb)

    await viber.send_message(
        sender_id,
        messages.KeyboardMessage(
            text=texts.ASKING_REPAIRS, keyboard=repairs_kb, min_api_version="3"
        ),
    )

    return await state.set_state(FullRepairsStates.waiting_address)


async def report_issue(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    sender_id = request.sender.id
    await update_last_message(sender_id, texts.ASKING_TECH_PROBLEMS, back_kb)

    await viber.send_message(
        sender_id,
        messages.KeyboardMessage(text=texts.ASKING_TECH_PROBLEMS, keyboard=back_kb),
    )
    return await state.set_state(FullIssueReportStates.waiting_issue_report)


async def create_request(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    user_id = (await state.get_data()).get("UserId")

    sender_id = request.sender.id

    await viber.send_message(
        sender_id,
        messages.TextMessage(text="Завантажую теми для звернень"),
    )

    problems = await HttpChatBot.get_problems(UserIdDto(user_id=user_id))

    await state.update_data(Problems=problems)

    kb = generate_problem_kb(problems)

    await viber.send_message(
        sender_id,
        messages.KeyboardMessage(text=texts.ASKING_PROBLEM, keyboard=kb),
    )

    await update_last_message(sender_id, texts.ASKING_PROBLEM, kb)

    await state.set_state(CreateRequestStates.waiting_problem)


async def actual_requests(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)
    user_data = await state.get_data()

    sender_id = request.sender.id

    await viber.send_message(sender_id, messages.TextMessage(text=texts.LOADING))

    user_reqs = await HttpChatBot.actual_requests(UserIdDto(user_id=user_data.get("UserId")))

    await viber.send_message(sender_id, messages.TextMessage(text="Звернення які розглядаються"))

    for user_req in user_reqs:
        template_data = {
            "id": user_req.get("Id"),
            "problem": user_req.get("Problem"),
            "reason": user_req.get("Reason"),
            "address": f"{user_req.get('Street')} {user_req.get('House')}",
            "comment": user_req.get("Text"),
        }

        template = render_template("actual_requests.j2", data=template_data)

        await viber.send_message(sender_id, messages.TextMessage(text=template))

    return await full_cabinet_menu(request, data)


async def history_requests(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    sender_id = request.sender.id

    await viber.send_message(sender_id, messages.TextMessage(text=texts.LOADING))

    user_id = (await state.get_data()).get("UserId")
    archived_reqs = await HttpChatBot.archived_requests(UserIdDto(user_id=user_id))

    if len(archived_reqs) == 0:
        await viber.send_message(sender_id, messages.TextMessage(text="Архівованих заявок немає."))
        await full_cabinet_menu(request, data)
        return

    kb = generate_archive_req_kb(archived_reqs)
    await update_last_message(sender_id, "Показую архівовані заявки", kb)

    await viber.send_message(
        sender_id,
        messages.KeyboardMessage(text="Показую архівовані заявки", keyboard=kb),
    )

    await state.update_data(ArchiveRequests=archived_reqs)

    await state.set_state(ArchiveRequestsStates.waiting_req)


async def reference_info(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    await ReferenceInfoHandlers.load_menu(
        request=request, state=state, parent_id=None, new_state=FullReferenceInfoStates.waiting_info
    )


async def send_edit_user_info(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)
    user_data = await state.get_data()

    data = {
        "FirstName": user_data.get("FirstName"),
        "LastName": user_data.get("LastName"),
        "MiddleName": user_data.get("MiddleName"),
        "Street": user_data.get("Street"),
        "House": user_data.get("House"),
        "Flat": user_data.get("Flat"),
        "Gender": Gender.get_label(user_data.get("Gender")),
    }

    await state.set_state(FullEditInfoStates.waiting_acceptation)

    template = render_template("edit_user_info.j2", data=data)

    sender_id = request.sender.id

    await update_last_message(sender_id, template, edit_profile_kb)

    await viber.send_message(
        sender_id, messages.KeyboardMessage(text=template, keyboard=edit_profile_kb)
    )


async def rate_enterprises(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    async def get_enterprises():
        user_id = (await state.get_data()).get("UserId")
        return await HttpChatBot.get_enterprises(UserIdDto(user_id=user_id))

    async def menu_callback():
        return await full_cabinet_menu(request, data)

    return await EnterprisesHandlers.enterprises_list(
        request=request,
        state=state,
        get_enterprises=get_enterprises,
        new_state=FullRateEnterpriseStates.showing_list,
        menu_callback=menu_callback,
    )
