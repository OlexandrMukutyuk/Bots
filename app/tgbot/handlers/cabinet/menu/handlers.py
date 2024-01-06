from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboards.default.cabinet import cabinet_menu_text, cabinet_menu_kb
from keyboards.default.cabinet.edit_profile import edit_profile_kb
from keyboards.inline.cabinet.archived_req import pick_archive_req_kb
from keyboards.inline.cabinet.cabinet import share_chatbot_kb
from keyboards.inline.cabinet.create_request import pick_problem_kb
from keyboards.inline.cabinet.rate_enterprises import enterprises_list_kb
from services import http_client
from states.cabinet import IssueReportStates, ShareChatbot, CabinetStates, CreateRequest, RateEnterprise, \
    ArchiveRequests, EditInfo


async def show_cabinet_menu(message: types.Message, state: FSMContext):
    return await give_cabinet_menu(state=state, message=message)


async def give_cabinet_menu(
        state: FSMContext,
        **kwargs
):
    await state.set_state(CabinetStates.waiting_menu)

    message: types.Message = kwargs.get('message')

    if message:
        await message.answer('Чим можу допомогти? 👇', reply_markup=cabinet_menu_kb)
    else:
        bot: Bot = kwargs.get('bot')
        chat_id: int = kwargs.get('chat_id')

        await bot.send_message(chat_id, 'Чим можу допомогти? 👇', reply_markup=cabinet_menu_kb)


async def main_handler(message: types.Message, state: FSMContext):
    button_text = message.text

    if button_text == cabinet_menu_text['create_request']:
        return await create_request(message, state)

    if button_text == cabinet_menu_text['actual_requests']:
        return await actual_requests(message, state)

    if button_text == cabinet_menu_text['report_issue']:
        return await report_issue(message, state)

    if button_text == cabinet_menu_text['share_chatbot']:
        return await share_chatbot(message, state)

    if button_text == cabinet_menu_text['review_enterprises']:
        return await rate_enterprises(message, state)

    if button_text == cabinet_menu_text['history_requests']:
        return await history_requests(message, state)

    if button_text == cabinet_menu_text['change_user_info']:
        return await change_user_info(message, state)


async def report_issue(message: types.Message, state: FSMContext):
    await message.answer(
        text='Напишіть текст звернення про технічні негаразди на порталі',
        reply_markup=ReplyKeyboardRemove()
    )
    return await state.set_state(IssueReportStates.waiting_issue_report)


async def share_chatbot(message: types.Message, state: FSMContext):
    await message.answer('Поділіться чат-ботом', reply_markup=ReplyKeyboardRemove())
    await message.answer('Використовуйте кнопки нижче 👇', reply_markup=share_chatbot_kb)

    return await state.set_state(ShareChatbot.waiting_back)


async def create_request(message: types.Message, state: FSMContext):
    loading = await message.answer('Завантажую теми для звернень', reply_markup=ReplyKeyboardRemove())

    user_id = (await state.get_data()).get('UserId')

    problems = await http_client.get_problems(user_id)

    await loading.delete()

    await state.update_data(Problems=problems)

    problems_message = await message.answer('Виберіть тему проблеми, яка у вас виникла 👇', reply_markup=pick_problem_kb)

    await state.update_data(ProblemsMessageId=problems_message.message_id)

    await state.set_state(CreateRequest.waiting_problem)


async def actual_requests(message: types.Message, state: FSMContext):
    user_data = await state.get_data()

    temp_msg = await message.answer("Завантаження...")

    requests = await http_client.actual_requests(user_id=user_data.get('UserId'))

    await temp_msg.delete()
    await message.answer('Звернення які розглядаються')

    for request in requests:
        id = request.get('Id')
        problem = request.get('Problem')
        reason = request.get('Reason')
        address = f"{request.get('Street')} {request.get('House')}"
        comment = request.get('Text')

        text = [
            f"Звернення № {id}",
            f"Проблема: {problem}",
            f"Причина: {reason}\n",
            f"Адреса: {address}\n",
            f"{comment}",
        ]

        await message.answer('\n'.join(text))

    return await give_cabinet_menu(state=state, message=message)


async def rate_enterprises(message: types.Message, state: FSMContext):
    user_data = await state.get_data()

    temp_msg = await message.answer('Завантажую дані...', reply_markup=ReplyKeyboardRemove())

    enterprises = await http_client.get_enterprises(user_id=user_data.get('UserId'))

    allowed_to_rate = list(filter(lambda item: item.get('CanVote'), enterprises))

    await temp_msg.delete()

    if len(allowed_to_rate) == 0:
        await message.answer('Наразі для вас немає доступних для оцінювання підприємст')
        return await give_cabinet_menu(message=message, state=state)

    await message.answer(
        text='Оберіть підприємство, яке ви хотіли би оцінити ⭐️',
        reply_markup=enterprises_list_kb(allowed_to_rate)
    )

    await state.set_state(RateEnterprise.showing_list)


async def history_requests(message: types.Message, state: FSMContext):
    loading = await message.answer('Завантажую архівовані звернення', reply_markup=ReplyKeyboardRemove())

    user_id = (await state.get_data()).get('UserId')

    archived_req = await http_client.archived_requests(user_id)

    await loading.delete()

    if len(archived_req) == 0:
        await message.answer('Архівованих заявок немає.')
        return await give_cabinet_menu(state=state, message=message)

    await message.answer('Показую архівовані заявки', reply_markup=ReplyKeyboardRemove())

    req_msg = await message.answer(
        text='Виберіть звернення з кнопок нижче',
        reply_markup=pick_archive_req_kb
    )

    await state.update_data(
        ArchiveRequests=archived_req,
        ArchiveRequestsMessageId=req_msg.message_id
    )

    await state.set_state(ArchiveRequests.waiting_req)


async def change_user_info(message: types.Message, state: FSMContext):
    return await send_edit_user_info(state, message=message)


async def send_edit_user_info(state: FSMContext, **kwargs):
    user_data = await state.get_data()

    flat = ''
    if user_data.get('Flat'):
        flat = f"Квартира: {user_data.get('Flat')}\n"

    if user_data.get('Gender') == 'male':
        gender = 'Чоловік'
    elif user_data.get('Gender') == 'female':
        gender = 'Жінка'
    else:
        gender = "Не вказано"

    info_text = (
        'Ваші дані\n\n'
        f"Ім'я: {user_data.get('FirstName')}\n"
        f"Прізвище: {user_data.get('LastName')}\n"
        f"По батькові: {user_data.get('MiddleName')}\n"
        f"Вулиця: {user_data.get('Street')}\n"
        f"Номер будинку: {user_data.get('House')}\n"
        f"{flat}"
        f"Стать: {gender}\n"
    )

    await state.set_state(EditInfo.waiting_acception)

    message: types.Message = kwargs.get('message')

    if message:
        await message.answer(text=info_text, reply_markup=edit_profile_kb)
    else:
        bot: Bot = kwargs.get('bot')
        chat_id: int = kwargs.get('chat_id')

        await bot.send_message(chat_id=chat_id, text=info_text, reply_markup=edit_profile_kb)
