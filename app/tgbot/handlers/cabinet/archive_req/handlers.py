from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from app.tgbot.handlers.cabinet.handlers import back_to_menu
from app.tgbot.handlers.cabinet.menu.handlers import give_cabinet_menu
from app.tgbot.keyboards.default.cabinet.archive_req import rate_request_kb
from app.tgbot.keyboards.inline.cabinet.archived_req import confirm_archive_req_kb
from app.tgbot.keyboards.inline.callbacks import ArchiveReqCallbackFactory
from app.tgbot.services import http_client
from app.tgbot.states.cabinet import ArchiveRequests


async def archive_req_list(callback: types.InlineQuery, state: FSMContext):
    requests = (await state.get_data()).get('ArchiveRequests')

    results = []

    for req in requests:
        id = req.get('Id')

        comment = req.get('Text')
        reason = req.get('Reason')

        title = f'{req.get('Problem')} #{id}'
        address = f'{req.get('Street')}, {req.get('House')}'

        results.append(types.InlineQueryResultArticle(
            id=str(id),
            title=title,
            input_message_content=types.InputTextMessageContent(
                message_text='\n'.join([
                    title,
                    f'🏙️ {address}',
                    f'📚 Причина: {reason}\n\n'
                    f'{comment}\n',
                    'Підтверджуйте 👇'
                ])
            ),
            reply_markup=confirm_archive_req_kb(req_id=id, can_review=len(req.get('Answers')) == 0)
        ))

    await callback.answer(results=results, cache_time=2)


async def delete_list_message(message: types.Message, state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    chat_id = message.chat.id

    await bot.delete_message(chat_id=chat_id, message_id=user_data.get('ArchiveRequestsMessageId'))

    await state.update_data(ArchiveRequestMessageId=message.message_id)


async def handdle_archive_req(
        callback: types.CallbackQuery,
        callback_data: ArchiveReqCallbackFactory,
        state: FSMContext,
        bot: Bot
):
    data = await state.get_data()
    review = callback_data.review
    req_id = callback_data.req_id

    chat_id = callback.from_user.id

    if review:

        await state.update_data(RequestReviewId=req_id)

        await bot.send_message(
            chat_id=chat_id,
            text=f'Дайте оцінку роботам по зверненню #{req_id}',
            reply_markup=rate_request_kb
        )

        await bot.delete_message(chat_id=chat_id, message_id=data.get('ArchiveRequestMessageId'))

        return await state.set_state(ArchiveRequests.waiting_rate)

    else:
        current_req: dict = {}

        archive_reqs = data.get('ArchiveRequests')

        for req in archive_reqs:
            if req.get('Id') == req_id:
                current_req = req

        await bot.send_message(
            chat_id=chat_id,
            text='\n'.join([
                f'Деталі звернення #{current_req.get('Id')}',
                f'Проблема: {current_req.get('Problem')}',
                f'Причина: {current_req.get('Reason')}',
                f'Адреса: {current_req.get('Street')}, {current_req.get('House')}',
                f'{current_req.get('Text')}'
            ])
        )

        await bot.delete_message(chat_id=chat_id, message_id=data.get('ArchiveRequestMessageId'))

        return await back_to_menu(callback=callback, state=state, bot=bot)


async def back_to_main_menu(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    chat_id = callback.from_user.id

    await bot.delete_message(chat_id=chat_id, message_id=data.get('ArchiveRequestMessageId'))

    await bot.send_message(chat_id=chat_id, text='Повертаємось до меню')

    return await back_to_menu(callback=callback, state=state, bot=bot)


async def save_rate(message: types.Message, state: FSMContext):
    text = message.text

    rate = min(5, text.count('⭐'))

    await state.update_data(RequestRate=rate)
    await state.set_state(ArchiveRequests.waiting_comment)

    await message.answer('Ваша оцінка прийнята')
    await message.answer('Напишіть свій коментар ⬇️', reply_markup=ReplyKeyboardRemove())


async def save_comment(message: types.Message, state: FSMContext):
    data = await state.get_data()

    comment = message.text

    print({
        "RequestId": data.get('RequestReviewId'),
        "Mark": data.get('RequestRate'),
        "Comment": comment
    })

    await http_client.rate_request({
        "RequestId": data.get('RequestReviewId'),
        "Mark": data.get('RequestRate'),
        "Comment": comment
    })

    await message.answer('Ви успішно оцінили виконня запиту')

    return await give_cabinet_menu(state, message=message)


async def continue_later(message: types.Message, state: FSMContext):
    await message.answer('Ви завжди зможете оцінити виконання в розділі "Історія звернень"')
    await give_cabinet_menu(state, message=message)
