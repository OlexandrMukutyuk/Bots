import os

from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from data import config
from handlers.cabinet.handlers import back_to_menu
from handlers.cabinet.menu.handlers import give_cabinet_menu
from handlers.common import delete_tmp_media, update_user_state_data, generate_inline_street_list
from keyboards.default.basic import yes_n_no, yes
from keyboards.default.cabinet.create_request import request_yes_no_kb, request_flat_kb, \
    request_images_kb, living_in_house, request_comment_kb, request_house_kb, back_text, no_need, enough_text, \
    request_manual_address_kb, request_back_and_main_kb, request_enough_kb
from keyboards.inline.cabinet.create_request import confirm_problem_kb, pick_reason_kb, confirm_reason_kb
from keyboards.inline.callbacks import ProblemCallbackFactory, StreetCallbackFactory
from keyboards.inline.streets import choose_street_kb
from services import http_client
from services.http_client import fetch_streets
from states.cabinet import CabinetStates, CreateRequest


# Choose problem from list

async def show_problems_list(callback: types.InlineQuery, state: FSMContext):
    problems = (await state.get_data()).get('Problems')

    results = []

    for item in problems:
        id = item['Id']
        name = item['Name']

        results.append(types.InlineQueryResultArticle(
            id=str(id),
            title=name,
            input_message_content=types.InputTextMessageContent(
                message_text=f"{name}\n\nПідтверджуйте 👇"
            ),
            reply_markup=confirm_problem_kb(problem_id=id)
        ))

    await callback.answer(results=results, cache_time=2)


async def save_problem_message(message: types.Message, state: FSMContext):
    await state.update_data(ProblemsConfirmMessageId=message.message_id)


async def confirm_problem(
        callback: types.CallbackQuery,
        callback_data: ProblemCallbackFactory,
        state: FSMContext,
        bot: Bot
):
    data = await state.get_data()

    chat_id = callback.from_user.id
    problem_id = callback_data.problem_id

    await delete_inline_message(
        bot=bot,
        chat_id=chat_id,
        msg_id=data.get('ProblemsMessageId'),
        msg_confirm_id=data.get('ProblemsConfirmMessageId')
    )

    problems = await http_client.get_problems(user_id=data.get('UserId'))
    problem_name = ''

    for problem in problems:
        if problem.get('Id') == problem_id:
            problem_name = problem.get('Name')

    await state.update_data(
        ProblemId=problem_id,
        ProblemName=problem_name
    )

    await state.set_state(CreateRequest.waiting_reason)

    await bot.send_message(chat_id=chat_id, text='Тема прийнята. Завантажуємо підтеми...')

    response = await http_client.get_reasons(problem_id=problem_id)

    await state.update_data(Reasons=response)

    reasons_message = await bot.send_message(
        chat_id=chat_id,
        text='Виберіть підтему проблеми, яка у вас виникла 👇',
        reply_markup=pick_reason_kb
    )

    await state.update_data(ReasonsMessageId=reasons_message.message_id)

    return await callback.answer()


async def cancel_problem(callback: types.CallbackQuery, state: FSMContext, bot: Bot) -> None:
    chat_id = callback.from_user.id
    data = await state.get_data()

    await bot.delete_message(chat_id, data.get('ProblemsMessageId'))
    await bot.delete_message(chat_id, data.get('ProblemsConfirmMessageId'))

    await bot.send_message(chat_id=chat_id, text='Повертаємось до меню')

    return await back_to_menu(callback=callback, state=state, bot=bot)


# Choose reason from list

async def show_reasons_list(callback: types.InlineQuery, state: FSMContext):
    problems = (await state.get_data()).get('Reasons')

    results = []

    for item in problems:
        id = item['Id']
        name = item['Name']

        results.append(types.InlineQueryResultArticle(
            id=str(id),
            title=name,
            input_message_content=types.InputTextMessageContent(
                message_text=f"{name}\n\nПідтверджуйте 👇"
            ),
            reply_markup=confirm_reason_kb(reason_id=id)
        ))

    await callback.answer(results=results, cache_time=2)


async def save_reason_message(message: types.Message, state: FSMContext):
    await state.update_data(ReasonConfirmMessageId=message.message_id)


async def confirm_reason(
        callback: types.CallbackQuery,
        callback_data: ProblemCallbackFactory,
        state: FSMContext,
        bot: Bot
):
    chat_id = callback.from_user.id
    reason_id = callback_data.problem_id

    data = await state.get_data()

    await delete_inline_message(
        bot=bot,
        chat_id=chat_id,
        msg_id=data.get('ReasonsMessageId'),
        msg_confirm_id=data.get('ReasonConfirmMessageId')
    )

    reasons = await http_client.get_reasons(problem_id=data.get('ProblemId'))
    reason_name = ''

    for reason in reasons:
        if reason.get('Id') == reason_id:
            reason_name = reason.get('Name')

    await state.update_data(ReasonId=reason_id, ReasonName=reason_name)

    await state.set_state(CreateRequest.waiting_address)

    await bot.send_message(chat_id=chat_id, text='Підтема прийнята')

    street = data.get("Street")
    house = data.get("House")

    await bot.send_message(
        chat_id=chat_id,
        text=f"Місце де все трапилось {street} {house}?",
        reply_markup=request_yes_no_kb
    )

    return await callback.answer()


async def cancel_reason(callback: types.CallbackQuery, state: FSMContext, bot: Bot) -> None:
    chat_id = callback.from_user.id

    data = await state.get_data()

    await bot.delete_message(chat_id, data.get('ReasonsMessageId'))
    await bot.delete_message(chat_id, data.get('ReasonConfirmMessageId'))

    sub_problem_message = await bot.send_message(
        chat_id=chat_id,
        text='Виберіть підтему проблеми, яка у вас виникла 👇',
        reply_markup=pick_reason_kb
    )

    await state.update_data(ReasonsMessageId=sub_problem_message.message_id)


# Choose Address

async def request_on_my_house(message: types.Message, state: FSMContext):
    data = await state.get_data()

    user_city_id = data.get("CityId")
    user_city_name = data.get("City")
    user_street_id = data.get("StreetId")
    user_street_name = data.get("Street")
    user_house = data.get("House")

    await state.update_data({
        **data,
        'RequestCityId': user_city_id,
        'RequestStreetId': user_street_id,
        'RequestHouse': user_house,

        'RequestStreetName': user_street_name,
        'RequestCityName': user_city_name,
    })

    return await ask_flat(message, state)


async def manually_type_location(message: types.Message, state: FSMContext):
    await state.set_state(CreateRequest.is_address_manually)

    await message.answer(
        text='Ви можете поділитися геолокацією, або вписати адресу вручну. Передача гео не працює з ПК.',
        reply_markup=request_manual_address_kb
    )


async def location_by_geo(message: types.Message, state: FSMContext):
    user_data = await state.get_data()

    lng = message.location.longitude
    lat = message.location.latitude
    user_id = user_data.get("UserId")

    address_info = await http_client.get_address_by_geo(
        user_id=user_id,
        lat=lat,
        lng=lng
    )

    if not address_info:
        return await message.answer(
            text='Виникла помилка з запитом. Спробувати ще раз?',
            reply_markup=yes_n_no
        )

    user_city_id = user_data.get("CityId")
    user_city_name = user_data.get("City")

    user_street_id = address_info.get("StreetId")
    user_street_name = address_info.get("StreetName")
    user_house = address_info.get("House")

    await state.update_data({
        **user_data,
        'RequestCityId': user_city_id,
        'RequestStreetId': user_street_id,
        'RequestHouse': user_house,

        'RequestStreetName': user_street_name,
        'RequestCityName': user_city_name,
    })

    return await ask_flat(message, state)


async def ask_for_street_name(message: types.Message, state: FSMContext):
    await state.set_state(CreateRequest.waiting_street_typing)
    await message.answer(
        text='Впишіть назву вулиці де все трапилось (мінімум 3 літери) 🏙️',
        reply_markup=request_back_and_main_kb
    )


async def choose_street(message: types.Message, state: FSMContext):
    streets_data = await fetch_streets(message.text)

    if len(streets_data) == 0:
        await message.answer("Пошук не дав результатів")
        return await message.answer("Впишіть назву вашої вулиці (мінімум 3 літери) 🏙️")

    message = await message.answer('Виберіть вулицю з кнопок нижче! 👇', reply_markup=choose_street_kb)

    await state.update_data(Streets=streets_data)
    await state.update_data(StreetsMessageId=message.message_id)

    await state.set_state(CreateRequest.waiting_street_selected)


async def show_street_list(callback: types.InlineQuery, state: FSMContext):
    data = await state.get_data()

    await generate_inline_street_list(data, callback)


async def save_street_message(message: types.Message, state: FSMContext):
    await state.update_data(StreetConfirmMessageId=message.message_id)


async def confirm_street(
        callback: types.CallbackQuery,
        callback_data: StreetCallbackFactory,
        state: FSMContext,
        bot: Bot
):
    data = await state.get_data()
    chat_id = callback.from_user.id

    street = await http_client.get_street_by_id(callback_data.street_id)

    await state.update_data(
        Streets=None,
        RequestStreetId=callback_data.street_id,
        RequestStreetName=street.get('name'),
        RequestCityId=callback_data.city_id,
    )

    await delete_inline_message(
        bot=bot,
        chat_id=chat_id,
        msg_id=data.get('StreetsMessageId'),
        msg_confirm_id=data.get('StreetConfirmMessageId')
    )

    await bot.send_message(
        chat_id=callback.from_user.id,
        text="Впишіть будь ласка номер будинку 🏠",
        reply_markup=request_house_kb
    )

    await state.set_state(CreateRequest.waiting_house)

    return await callback.answer()


async def save_house(message: types.Message, state: FSMContext):
    house = message.text

    street_id = (await state.get_data())["RequestStreetId"]

    is_address_correct = await http_client.verify_address(street_id=street_id, house=house)

    if not is_address_correct:
        await message.answer("Такого будинку не знайдено")
        return await message.answer(
            text="Впишіть будь ласка номер будинку 🏠",
            reply_markup=request_house_kb
        )

    await state.update_data(RequestHouse=house)

    return await ask_flat(message, state)


async def change_street(message: types.Message, state: FSMContext):
    await state.set_state(CreateRequest.waiting_street_typing)
    await message.answer('Впишіть назву вашої вулиці (мінімум 3 літери) 🏙️', reply_markup=ReplyKeyboardRemove())


async def ask_flat(message: types.Message, state: FSMContext):
    await state.set_state(CreateRequest.waiting_flat)
    await message.answer(
        text='Впишіть номер квартири. (Якщо мешкаєте у своєму домі, жміть кнопку знизу)',
        reply_markup=request_flat_kb
    )


async def save_flat(message: types.Message, state: FSMContext):
    text = message.text

    if text == living_in_house:
        text = None

    await state.update_data(RequestFlat=text)

    await message.answer(
        text='Залиште коментар стосовно проблеми',
        reply_markup=request_comment_kb
    )

    await state.set_state(CreateRequest.waiting_comment)


# Other handlers


async def save_comment(message: types.Message, state: FSMContext):
    text = message.text

    if text == back_text:
        return await ask_flat(message, state)

    await state.update_data(Comment=text)

    await message.answer(
        text='Потрібно відображати цю проблему на сайті?',
        reply_markup=request_yes_no_kb
    )

    await state.set_state(CreateRequest.waiting_showing_status)


async def save_showing_status(message: types.Message, state: FSMContext):
    text = message.text

    if text == yes:
        show_on_site = True
    else:
        show_on_site = False

    await state.update_data(ShowOnSite=show_on_site)

    await message.answer(
        text='Прикріпляйте фото якщо необхідно',
        reply_markup=request_images_kb
    )

    await message.answer('Тільки по одному')

    await state.set_state(CreateRequest.waiting_images)


async def saving_images(message: types.Message, state: FSMContext, bot: Bot):
    text = message.text

    if text in [no_need, enough_text]:
        return await showing_request_info(message, state)

    data = await state.get_data()

    images = data.get('RequestImages') or []

    new_image = f"{message.photo[-1].file_id}.jpg"

    await state.update_data(RequestImages=[*images, new_image])

    await bot.download(
        message.photo[-1],
        destination=f"{os.getcwd()}/tmp/{new_image}"
    )

    await message.answer('Завантажуйте ще', reply_markup=request_enough_kb)


async def showing_request_info(message: types.Message, state: FSMContext):
    await state.set_state(CreateRequest.waiting_confirm)
    data = await state.get_data()

    if data.get('ShowOnSite'):
        photo_text = 'Відображати на сайті'
    else:
        photo_text = 'Не відображати на сайті'

    flat_text = ''
    if data.get('RequestFlat'):
        flat_text = f"Квартира: {data.get('RequestFlat')}"

    text = [
        'Звернення:\n',
        f"Проблема: {data.get('ProblemName')}",
        f"Причина: {data.get('ReasonName')}",
        f"Коментар: {data.get('Comment')}",
        f"{photo_text}",
        f"Завантажено {len(data.get('RequestImages') or [])} фото",
        f"Вулиця: {data.get('RequestStreetName')}",
        f"Будинок: {data.get('RequestHouse')}",
        flat_text
    ]

    await message.answer('\n'.join(text))
    await message.answer('Відправити звернення?', reply_markup=yes_n_no)


async def confirm_request(message: types.Message, state: FSMContext):
    temp_message = await message.answer('Відправляємо звернення', reply_markup=ReplyKeyboardRemove())

    user_data = await state.get_data()

    request_photos = user_data.get('RequestImages') or []
    photos_urls = []

    for photo in request_photos:
        photos_urls.append(f"{config.WEBHOOK_ADDRESS}/media/{photo}")

    request_id = await http_client.create_request({
        "UserId": user_data.get('UserId'),
        "ProblemId": user_data.get('ProblemId'),
        "ReasonId": user_data.get('ReasonId'),
        "CityId": user_data.get('RequestCityId'),
        "StreetId": user_data.get('RequestStreetId'),
        "House": user_data.get('RequestHouse'),
        "Flat": user_data.get('RequestFlat'),
        "Comment": user_data.get('Comment'),
        "ShowOnSite": user_data.get('ShowOnSite'),
        "Photos": photos_urls
    })

    await temp_message.delete()

    if not request_id:
        return await message.answer(
            text='Виникла помилка з запитом. Спробувати ще раз?',
            reply_markup=yes_n_no
        )

    await message.answer(f"Звернення №{request_id} відправлено успішно!")

    await to_main_menu_reply(message, state)


# To main menu handlers

async def to_main_menu_inline(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    chat_id = callback.from_user.id

    await reset_user_request_state(state, bot=bot, chat_id=chat_id)


async def to_main_menu_reply(message: types.Message, state: FSMContext):
    await reset_user_request_state(state, message=message)


async def reset_user_request_state(state: FSMContext, **kwargs):
    message: types.Message = kwargs.get("message")
    bot: Bot = kwargs.get("bot")
    chat_id: int = kwargs.get("chat_id")

    if message:
        await give_cabinet_menu(state=state, message=message)
    else:
        await give_cabinet_menu(state=state, bot=bot, chat_id=chat_id)

    user_data = await state.get_data()
    request_photos = user_data.get('RequestImages')

    delete_tmp_media(request_photos)

    await update_user_state_data(state)

    await state.set_state(CabinetStates.waiting_menu)


# Back handlers


async def manually_address_back(message: types.Message, state: FSMContext, bot: Bot):
    chat_id = message.chat.id
    data = await state.get_data()

    await state.set_state(CreateRequest.waiting_address)

    await bot.send_message(chat_id=chat_id, text='Підтема прийнята')

    street = data.get("Street")
    house = data.get("House")

    await bot.send_message(
        chat_id=chat_id,
        text=f"Місце де все трапилось {street} {house}?",
        reply_markup=request_yes_no_kb
    )


async def street_back(message: types.Message, state: FSMContext):
    await state.set_state(CreateRequest.is_address_manually)

    await message.answer(
        text='Потрібно відображати цю проблему на сайті?',
        reply_markup=request_yes_no_kb
    )


async def flat_back(message: types.Message, state: FSMContext):
    await state.set_state(CreateRequest.waiting_reason)
    await message.answer(reply_markup=ReplyKeyboardRemove(), text='Добре')
    message = await message.answer(
        text='Виберіть підтему проблеми, яка у вас виникла 👇',
        reply_markup=pick_reason_kb
    )

    return await state.update_data(ReasonsMessageId=message.message_id)


async def comment_back(message: types.Message, state: FSMContext):
    await ask_flat(message, state)


async def showing_status_back(message: types.Message, state: FSMContext):
    await state.set_state(CreateRequest.waiting_comment)
    return await message.answer(
        text='Залиште коментар стосовно проблеми',
        reply_markup=request_comment_kb
    )


async def saving_images_back(message: types.Message, state: FSMContext):
    await state.set_state(CreateRequest.waiting_showing_status)

    await message.answer(
        text='Потрібно відображати цю проблему на сайті?',
        reply_markup=request_yes_no_kb
    )


# Helpers


async def delete_inline_message(bot: Bot, chat_id: int, msg_id: int, msg_confirm_id: int):
    try:
        await bot.delete_message(chat_id, msg_id)
        await bot.delete_message(chat_id, msg_confirm_id)
    except Exception:
        print("Messages not found")
