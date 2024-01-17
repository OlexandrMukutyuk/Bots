from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from dto.chat_bot import RateRequestDto
from handlers.advanced.cabinet.common import back_to_menu
from handlers.advanced.cabinet.menu.handlers import give_cabinet_menu
from handlers.common.inline_mode import InlineHandlers
from keyboards.default.cabinet.archive_req import rate_request_kb
from keyboards.inline.cabinet.archived_req import confirm_archive_req_kb
from keyboards.inline.callbacks import ArchiveReqCallbackFactory
from services.http_client import HttpChatBot
from states.advanced import ArchiveRequestsStates
from utils.template_engine import render_template


async def archive_req_list(callback: types.InlineQuery, state: FSMContext):
    requests = (await state.get_data()).get("ArchiveRequests")

    def inline_markup(req: dict):
        data = {
            "ID": req.get("Id"),
            "Title": f"{req.get('Problem')} #{req.get('Id')}",
            "Comment": req.get("Text"),
            "Reason": req.get("Reason"),
            "Problem": f"{req.get('Problem')}",
            "Address": f"{req.get('Street')}, {req.get('House')}",
        }

        template = render_template("archive_requests.j2", data=data)

        return types.InlineQueryResultArticle(
            id=str(data.get("ID")),
            title=data.get("Title"),
            input_message_content=types.InputTextMessageContent(message_text=template),
            reply_markup=confirm_archive_req_kb(
                req_id=data.get("ID"), can_review=len(req.get("Answers")) == 0
            ),
        )

    return await InlineHandlers.generate_inline_list(
        callback=callback, data=requests, render_func=inline_markup
    )


async def delete_list_message(message: types.Message, state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    chat_id = message.chat.id

    await bot.delete_message(chat_id=chat_id, message_id=user_data.get("ArchiveRequestsMessageId"))

    await state.update_data(ArchiveRequestMessageId=message.message_id)


async def request_details(
    callback: types.CallbackQuery,
    callback_data: ArchiveReqCallbackFactory,
    state: FSMContext,
    bot: Bot,
):
    user_data = await state.get_data()
    req_id = callback_data.req_id
    chat_id = callback.from_user.id

    current_req: dict = {}

    archive_reqs = user_data.get("ArchiveRequests")

    for req in archive_reqs:
        if req.get("Id") == req_id:
            current_req = req

    data = {
        "Id": current_req.get("Id"),
        "Problem": current_req.get("Problem"),
        "Reason": current_req.get("Reason"),
        "Address": f"{current_req.get('Street')}, {current_req.get('House')}",
        "Text": current_req.get("Text"),
    }

    template = render_template("archive_requests_details.j2", data=data)

    await bot.send_message(chat_id=chat_id, text=template)

    await bot.delete_message(chat_id=chat_id, message_id=user_data.get("ArchiveRequestMessageId"))

    await back_to_menu(callback=callback, state=state, bot=bot)


async def review_request(
    callback: types.CallbackQuery,
    callback_data: ArchiveReqCallbackFactory,
    state: FSMContext,
    bot: Bot,
):
    data = await state.get_data()
    req_id = callback_data.req_id

    chat_id = callback.from_user.id

    await state.update_data(RequestReviewId=req_id)

    await bot.send_message(
        chat_id=chat_id,
        text=f"Дайте оцінку роботам по зверненню #{req_id}",
        reply_markup=rate_request_kb,
    )

    await bot.delete_message(chat_id=chat_id, message_id=data.get("ArchiveRequestMessageId"))
    await state.set_state(ArchiveRequestsStates.waiting_rate)


async def back_to_main_menu(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    chat_id = callback.from_user.id

    print(data.get("ArchiveRequestMessageId"))

    await bot.delete_message(chat_id=chat_id, message_id=data.get("ArchiveRequestMessageId"))
    await bot.send_message(chat_id=chat_id, text="Повертаємось до меню")

    return await back_to_menu(callback=callback, state=state, bot=bot)


async def save_rate(message: types.Message, state: FSMContext):
    text = message.text

    rate = min(5, text.count("⭐"))

    await state.update_data(RequestRate=rate)
    await state.set_state(ArchiveRequestsStates.waiting_comment)

    await message.answer("Ваша оцінка прийнята")
    await message.answer(text="Напишіть свій коментар ⬇️", reply_markup=ReplyKeyboardRemove())


async def save_comment(message: types.Message, state: FSMContext):
    data = await state.get_data()

    comment = message.text

    await HttpChatBot.rate_request(
        RateRequestDto(
            request_id=data.get("RequestReviewId"), mark=data.get("RequestRate"), comment=comment
        )
    )

    await message.answer("Ви успішно оцінили виконня запиту")

    return await give_cabinet_menu(state, message=message)


async def continue_later(message: types.Message, state: FSMContext):
    await message.answer('Ви завжди зможете оцінити виконання в розділі "Історія звернень"')
    await give_cabinet_menu(state, message=message)
