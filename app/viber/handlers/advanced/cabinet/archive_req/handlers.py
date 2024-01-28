import texts
from dto.chat_bot import RateRequestDto
from handlers.common.helpers import full_cabinet_menu
from keyboards.archive_requests import confirm_archive_req_kb, rate_request_kb
from services.database import update_last_message
from services.http_client import HttpChatBot
from states import ArchiveRequestsStates
from utils.template_engine import render_template
from viber import viber
from viberio.dispatcher.dispatcher import Dispatcher

from viberio.types import requests, messages


async def show_basic_info(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    text_list = request.message.text.split(":")

    request_id = int(text_list[1])
    can_review = bool(int(text_list[2]))

    archive_reqs = (await state.get_data()).get("ArchiveRequests")

    current_req = None
    for req in archive_reqs:
        if req.get("Id") == request_id:
            current_req = req

    data = {
        "ID": current_req.get("Id"),
        "Title": f"{current_req.get('Problem')} #{current_req.get('Id')}",
        "Comment": current_req.get("Text"),
        "Reason": current_req.get("Reason"),
        "Problem": f"{current_req.get('Problem')}",
        "Address": f"{current_req.get('Street')}, {current_req.get('House')}",
    }

    template = render_template("archive_requests.j2", data=data)
    kb = confirm_archive_req_kb(request_id, can_review)
    sender_id = request.sender.id

    await update_last_message(sender_id, template, kb)

    await viber.send_message(
        sender_id,
        messages.KeyboardMessage(
            text=template,
            keyboard=kb,
            min_api_version="4",
        ),
    )


async def request_details(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)
    user_data = await state.get_data()

    text_list = request.message.text.split(":")
    request_id = int(text_list[1])

    current_req: dict = {}

    archive_reqs = user_data.get("ArchiveRequests")

    for req in archive_reqs:
        if req.get("Id") == request_id:
            current_req = req

    data = {
        "Id": current_req.get("Id"),
        "Problem": current_req.get("Problem"),
        "Reason": current_req.get("Reason"),
        "Address": f"{current_req.get('Street')}, {current_req.get('House')}",
        "Text": current_req.get("Text"),
    }

    template = render_template("archive_requests_details.j2", data=data)
    sender_id = request.sender.id

    await viber.send_message(
        sender_id,
        messages.TextMessage(text=template),
    )

    await full_cabinet_menu(request, data)


async def review_request(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)
    data = await state.get_data()

    text_list = request.message.text.split(":")
    req_id = int(text_list[1])

    await state.update_data(RequestReviewId=req_id)

    sender_id = request.sender.id

    text = f"Дайте оцінку роботам по зверненню #{req_id}"
    await update_last_message(sender_id, text, rate_request_kb)

    await viber.send_message(
        sender_id,
        messages.KeyboardMessage(
            text=text,
            keyboard=rate_request_kb,
            min_api_version="4",
        ),
    )

    await state.set_state(ArchiveRequestsStates.waiting_rate)


async def save_rate(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    rate = request.message.text
    sender_id = request.sender.id

    if rate == texts.LATER:
        await viber.send_message(
            sender_id,
            messages.TextMessage(
                text='Ви завжди зможете оцінити виконання в розділі "Історія звернень"',
            ),
        )
        return await full_cabinet_menu(request, data)

    await state.update_data(RequestRate=rate)
    await state.set_state(ArchiveRequestsStates.waiting_comment)

    await update_last_message(sender_id, "Напишіть свій коментар ⬇️")

    await viber.send_messages(
        sender_id,
        [
            messages.TextMessage(
                text="Ваша оцінка прийнята",
            ),
            messages.TextMessage(
                text="Напишіть свій коментар ⬇️",
            ),
        ],
    )


async def save_comment(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)
    data = await state.get_data()

    comment = request.message.text

    await HttpChatBot.rate_request(
        RateRequestDto(
            request_id=data.get("RequestReviewId"), mark=data.get("RequestRate"), comment=comment
        )
    )

    sender_id = request.sender.id

    await viber.send_message(
        sender_id,
        messages.TextMessage(
            text="Ви успішно оцінили виконня запиту",
        ),
    )

    return await full_cabinet_menu(request, data)
