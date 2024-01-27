from dto.chat_bot import UserIdDto
from handlers.common.enterprises import EnterprisesHandlers
from handlers.common.helpers import full_cabinet_menu
from keyboards.cabinet import cabinet_menu_text
from keyboards.user import edit_profile_kb
from models import Gender
from services.http_client import HttpChatBot
from states import FullRateEnterpriseStates, FullEditInfoStates
from utils.template_engine import render_template
from viber import viber
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.types import requests, messages


async def main_handler(request: requests.ViberMessageRequest, data: dict):
    button_text = request.message.text
    #
    # if button_text == cabinet_menu_text["create_request"]:
    #     return await create_request(message, state)
    #
    # if button_text == cabinet_menu_text["actual_requests"]:
    #     return await actual_requests(message, state)
    #
    # if button_text == cabinet_menu_text["report_issue"]:
    #     return await report_issue(message, state)
    #
    # if button_text == cabinet_menu_text["share_chatbot"]:
    #     return await share_chatbot(message, state)

    if button_text == cabinet_menu_text["review_enterprises"]:
        return await rate_enterprises(request, data)
    #
    # if button_text == cabinet_menu_text["history_requests"]:
    #     return await history_requests(message, state)
    #
    if button_text == cabinet_menu_text["change_user_info"]:
        return await send_edit_user_info(request, data)

    # if button_text == cabinet_menu_text["reference_info"]:
    #     return await reference_info(message, state)
    #
    # if button_text == cabinet_menu_text["repairs"]:
    #     return await repairs(message, state)


# async def repairs(message: types.Message, state: FSMContext):
#     await message.answer(text=texts.REPAIRS, reply_markup=ReplyKeyboardRemove())
#     await message.answer(text=texts.ASKING_REPAIRS, reply_markup=repairs_kb)
#
#     return await state.set_state(FullRepairsStates.waiting_address)
#
#
# async def report_issue(message: types.Message, state: FSMContext):
#     await message.answer(
#         text=texts.ASKING_TECH_PROBLEMS,
#         reply_markup=ReplyKeyboardRemove(),
#     )
#     return await state.set_state(FullIssueReportStates.waiting_issue_report)
#
#
# async def share_chatbot(message: types.Message, state: FSMContext):
#     await message.answer(text=texts.SHARE_BOT, reply_markup=ReplyKeyboardRemove())
#     await message.answer(text=texts.USE_BUTTONS, reply_markup=share_chatbot_kb)
#
#     return await state.set_state(FullShareChatbotStates.waiting_back)
#
#
# async def rate_enterprises(message: types.Message, state: FSMContext):
#     user_data = await state.get_data()
#     user_id = user_data.get("UserId")
#
#     loading_msg = await send_loading_message(message=message)
#
#     enterprises = await HttpChatBot.get_enterprises(UserIdDto(user_id=user_id))
#     allowed_to_rate = list(filter(lambda item: item.get("CanVote"), enterprises))
#
#     await loading_msg.delete()
#
#     if len(allowed_to_rate) == 0:
#         await message.answer(texts.NO_ENTERPRISES_TO_RATE)
#         await full_cabinet_menu(message=message, state=state)
#         return
#
#     await message.answer(
#         text=texts.ASKING_ENTERPRISE,
#         reply_markup=enterprises_list_kb(allowed_to_rate),
#     )
#
#     await state.set_state(FullRateEnterpriseStates.showing_list)
#
#
# async def create_request(message: types.Message, state: FSMContext):
#     loading_msg = await send_loading_message(message=message)
#
#     user_id = (await state.get_data()).get("UserId")
#
#     problems = await HttpChatBot.get_problems(UserIdDto(user_id=user_id))
#
#     await loading_msg.delete()
#
#     await state.update_data(Problems=problems)
#
#     problems_msg = await message.answer(text=texts.ASKING_PROBLEM, reply_markup=pick_problem_kb)
#
#     await state.update_data(ProblemsMessageId=problems_msg.message_id)
#     await state.set_state(CreateRequestStates.waiting_problem)
#
#
# async def actual_requests(message: types.Message, state: FSMContext):
#     user_data = await state.get_data()
#
#     loading_message = await send_loading_message(message=message)
#
#     requests = await HttpChatBot.actual_requests(UserIdDto(user_id=user_data.get("UserId")))
#
#     await loading_message.delete()
#     await message.answer("Звернення які розглядаються")
#
#     for request in requests:
#         data = {
#             "id": request.get("Id"),
#             "problem": request.get("Problem"),
#             "reason": request.get("Reason"),
#             "address": f"{request.get('Street')} {request.get('House')}",
#             "comment": request.get("Text"),
#         }
#
#         template = render_template("actual_requests.j2", data=data)
#
#         await message.answer(template)
#
#     return await full_cabinet_menu(state=state, message=message)
#
#
# async def history_requests(message: types.Message, state: FSMContext):
#     loading_msg = await send_loading_message(message=message)
#
#     user_id = (await state.get_data()).get("UserId")
#     archived_req = await HttpChatBot.archived_requests(UserIdDto(user_id=user_id))
#
#     await loading_msg.delete()
#
#     if len(archived_req) == 0:
#         await message.answer("Архівованих заявок немає.")
#         await full_cabinet_menu(state=state, message=message)
#         return
#
#     await message.answer(text="Показую архівовані заявки", reply_markup=ReplyKeyboardRemove())
#
#     req_msg = await message.answer(
#         text="Виберіть звернення з кнопок нижче", reply_markup=pick_archive_req_kb
#     )
#
#     await state.update_data(
#         ArchiveRequests=archived_req, ArchiveRequestsMessageId=req_msg.message_id
#     )
#
#     await state.set_state(ArchiveRequestsStates.waiting_req)
#
#
# async def change_user_info(message: types.Message, state: FSMContext):
#     return await send_edit_user_info(state, message=message)
#
#
# async def reference_info(message: types.Message, state: FSMContext):
#     await ReferenceInfoHandlers.load_menu(
#         state=state,
#         parent_id=None,
#         new_state=FullReferenceInfoStates.waiting_info,
#         message=message
#     )
#
#


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
    await viber.send_message(
        request.sender.id, messages.KeyboardMessage(text=template, keyboard=edit_profile_kb)
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
