import os

from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

import texts
from data import config
from dto.chat_bot import (
    ProblemIdDto,
    UserIdDto,
    AddressByGeoDto,
    CreateRequestDto,
)
from handlers.cabinet.common import back_to_menu
from handlers.cabinet.menu.handlers import give_cabinet_menu
from handlers.common.flat import FlatHandlers
from handlers.common.helpers import update_user_state_data
from handlers.common.house import HouseHandlers
from handlers.common.inline_mode import InlineHandlers
from handlers.common.streets import StreetsHandlers
from keyboards.default.basic import yes_n_no, yes
from keyboards.default.cabinet.create_request import (
    request_yes_no_kb,
    request_flat_kb,
    request_images_kb,
    request_comment_kb,
    request_house_kb,
    request_manual_address_kb,
    request_back_and_main_kb,
    request_enough_kb,
)
from keyboards.inline.cabinet.create_request import (
    confirm_problem_kb,
    pick_reason_kb,
    confirm_reason_kb,
)
from keyboards.inline.callbacks import ProblemCallbackFactory, StreetCallbackFactory
from services.http_client import HttpChatBot
from states.cabinet import CabinetStates, CreateRequest
from texts.keyboards import NO_NEED, ENOUGH, BACK
from utils.media import delete_tmp_media
from utils.template_engine import render_template


class ProblemHandlers:
    ListCallback = "ProblemsMessageId"
    ConfirmCallback = "ProblemMessageId"


async def show_problems_list(callback: types.InlineQuery, state: FSMContext):
    problems = (await state.get_data()).get("Problems")

    def render_func(item: dict):
        id = item.get("Id")
        name = item.get("Name")

        return types.InlineQueryResultArticle(
            id=str(id),
            title=name,
            input_message_content=types.InputTextMessageContent(
                message_text=render_template("confirm_problem.j2", title=name)
            ),
            reply_markup=confirm_problem_kb(problem_id=id),
        )

    return await InlineHandlers.generate_inline_list(
        callback, data=problems, render_func=render_func
    )


async def message_via_bot(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()

    await delete_message(bot, message.from_user.id, data.get(ProblemHandlers.ListCallback))

    await state.set_data({**data, ProblemHandlers.ConfirmCallback: message.message_id})


async def confirm_problem(
    callback: types.CallbackQuery,
    callback_data: ProblemCallbackFactory,
    state: FSMContext,
    bot: Bot,
):
    data = await state.get_data()

    chat_id = callback.from_user.id
    problem_id = callback_data.problem_id

    await delete_message(bot, callback.from_user.id, data.get(ProblemHandlers.ConfirmCallback))

    problems = await HttpChatBot.get_problems(UserIdDto(user_id=data.get("UserId")))
    problem_name = ""

    for problem in problems:
        if problem.get("Id") == problem_id:
            problem_name = problem.get("Name")

    await state.set_state(CreateRequest.waiting_reason)

    await bot.send_message(chat_id=chat_id, text="Тема прийнята. Завантажуємо підтеми...")

    response = await HttpChatBot.get_reasons(ProblemIdDto(problem_id=problem_id))

    reasons_msg = await bot.send_message(
        chat_id=chat_id,
        text=texts.ASKGING_REASON,
        reply_markup=pick_reason_kb,
    )

    await state.set_data(
        {
            **data,
            ProblemHandlers.ListCallback: reasons_msg.message_id,
            "Reasons": response,
            "ProblemId": problem_id,
            "ProblemName": problem_name,
        }
    )

    return await callback.answer()


async def cancel_problem(callback: types.CallbackQuery, state: FSMContext, bot: Bot) -> None:
    chat_id = callback.from_user.id
    data = await state.get_data()

    await bot.delete_message(chat_id, data.get(ProblemHandlers.ConfirmCallback))

    await bot.send_message(chat_id=chat_id, text="Повертаємось до меню")

    return await back_to_menu(callback=callback, state=state, bot=bot)


async def show_reasons_list(callback: types.InlineQuery, state: FSMContext):
    reasons = (await state.get_data()).get("Reasons")

    def render_func(item: dict):
        id = item.get("Id")
        name = item.get("Name")

        return types.InlineQueryResultArticle(
            id=str(id),
            title=name,
            input_message_content=types.InputTextMessageContent(
                message_text=render_template("confirm_problem.j2", title=name)
            ),
            reply_markup=confirm_reason_kb(reason_id=id),
        )

    return await InlineHandlers.generate_inline_list(
        callback, data=reasons, render_func=render_func
    )


async def confirm_reason(
    callback: types.CallbackQuery,
    callback_data: ProblemCallbackFactory,
    state: FSMContext,
    bot: Bot,
):
    chat_id = callback.from_user.id
    reason_id = callback_data.problem_id

    data = await state.get_data()

    await bot.delete_message(chat_id, data.get(ProblemHandlers.ConfirmCallback))

    reasons = await HttpChatBot.get_reasons(ProblemIdDto(problem_id=data.get("ProblemId")))
    reason_name = ""

    for reason in reasons:
        if reason.get("Id") == reason_id:
            reason_name = reason.get("Name")

    await state.set_state(CreateRequest.waiting_address)
    await state.set_data({"ReasonId": reason_id, "ReasonName": reason_name, **data})

    await bot.send_message(chat_id=chat_id, text="Підтема прийнята")

    street = data.get("Street")
    house = data.get("House")

    await bot.send_message(
        chat_id=chat_id,
        text=f"Місце де все трапилось {street} {house}?",
        reply_markup=request_yes_no_kb,
    )

    return await callback.answer()


async def cancel_reason(callback: types.CallbackQuery, state: FSMContext, bot: Bot) -> None:
    chat_id = callback.from_user.id

    data = await state.get_data()

    await bot.delete_message(chat_id, data.get(ProblemHandlers.ConfirmCallback))

    msg = await bot.send_message(
        chat_id=chat_id,
        text=texts.ASKGING_REASON,
        reply_markup=pick_reason_kb,
    )

    await state.set_data({ProblemHandlers.ListCallback: msg.message_id, **data})


async def request_on_my_site(message: types.Message, state: FSMContext):
    data = await state.get_data()

    user_city_id = data.get("CityId")
    user_city_name = data.get("City")
    user_street_id = data.get("StreetId")
    user_street_name = data.get("Street")
    user_house = data.get("House")

    await state.update_data(
        {
            **data,
            "CityId": user_city_id,
            "StreetId": user_street_id,
            "House": user_house,
            "Street": user_street_name,
            "City": user_city_name,
        }
    )

    return await ask_flat(message, state)


async def manually_type_location(message: types.Message, state: FSMContext):
    await state.set_state(CreateRequest.is_address_manually)

    await message.answer(
        text="Ви можете поділитися геолокацією, або вписати адресу вручну. Передача гео не працює з ПК.",
        reply_markup=request_manual_address_kb,
    )


async def location_by_geo(message: types.Message, state: FSMContext):
    user_data = await state.get_data()

    lng = message.location.longitude
    lat = message.location.latitude
    user_id = user_data.get("UserId")

    address_info = await HttpChatBot.get_address_by_geo(
        AddressByGeoDto(user_id=user_id, lat=lat, lng=lng)
    )

    if not address_info:
        return await message.answer(
            text="Виникла помилка з запитом. Спробувати ще раз?", reply_markup=yes_n_no
        )

    user_city_id = user_data.get("CityId")
    user_city_name = user_data.get("City")

    user_street_id = address_info.get("StreetId")
    user_street_name = address_info.get("StreetName")
    user_house = address_info.get("House")

    await state.update_data(
        {
            **user_data,
            "CityId": user_city_id,
            "StreetId": user_street_id,
            "House": user_house,
            "Street": user_street_name,
            "City": user_city_name,
        }
    )

    return await ask_flat(message, state)


async def ask_for_street_name(message: types.Message, state: FSMContext):
    await state.set_state(CreateRequest.waiting_street_typing)
    await message.answer(
        text=texts.ASKING_STREET,
        reply_markup=request_back_and_main_kb,
    )


async def choose_street(message: types.Message, state: FSMContext, bot: Bot):
    return await StreetsHandlers.choose_street(
        message=message, state=state, new_state=CreateRequest.waiting_street_selected, bot=bot
    )


async def show_street_list(callback: types.InlineQuery, state: FSMContext):
    streets_data = (await state.get_data()).get("Streets")

    return await StreetsHandlers.inline_list(callback, streets_data)


async def confirm_street(
    callback: types.CallbackQuery, callback_data: StreetCallbackFactory, state: FSMContext, bot: Bot
):
    async def action():
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=texts.ASKING_HOUSE,
            reply_markup=request_house_kb,
        )

        await state.set_state(CreateRequest.waiting_house)

    return await StreetsHandlers.confirm_street(
        callback=callback, callback_data=callback_data, state=state, action=action, bot=bot
    )


async def save_house(message: types.Message, state: FSMContext):
    async def callback():
        return await ask_flat(message, state)

    return await HouseHandlers.change_house(
        message, state, new_state=CreateRequest.waiting_street_typing, callback=callback
    )


async def change_street(message: types.Message, state: FSMContext):
    await state.set_state(CreateRequest.waiting_street_typing)
    await message.answer(text=texts.ASKING_STREET, reply_markup=ReplyKeyboardRemove())


async def ask_flat(message: types.Message, state: FSMContext):
    await state.set_state(CreateRequest.waiting_flat)
    await message.answer(
        text=texts.ASKING_HOUSE,
        reply_markup=request_flat_kb,
    )


async def save_flat(message: types.Message, state: FSMContext):
    async def callback():
        await message.answer(
            text="Залиште коментар стосовно проблеми", reply_markup=request_comment_kb
        )

    await FlatHandlers.change_flat(
        message=message, state=state, new_state=CreateRequest.waiting_comment, callback=callback
    )


# Other handlers


async def save_comment(message: types.Message, state: FSMContext):
    text = message.text

    if text == BACK:
        return await ask_flat(message, state)

    await state.update_data(Comment=text)

    await message.answer(
        text="Потрібно відображати цю проблему на сайті?", reply_markup=request_yes_no_kb
    )

    await state.set_state(CreateRequest.waiting_showing_status)


async def save_showing_status(message: types.Message, state: FSMContext):
    text = message.text

    if text == yes:
        show_on_site = True
    else:
        show_on_site = False

    await state.update_data(ShowOnSite=show_on_site)

    await message.answer(text="Прикріпляйте фото якщо необхідно", reply_markup=request_images_kb)

    await message.answer("Тільки по одному")

    await state.set_state(CreateRequest.waiting_images)


async def saving_images(message: types.Message, state: FSMContext, bot: Bot):
    text = message.text

    if text in [NO_NEED, ENOUGH]:
        return await showing_request_info(message, state)

    data = await state.get_data()

    images = data.get("RequestImages") or []

    new_image = f"{message.photo[-1].file_id}.jpg"

    await state.update_data(RequestImages=[*images, new_image])

    await bot.download(message.photo[-1], destination=f"{os.getcwd()}/tmp/{new_image}")

    await message.answer("Завантажуйте ще", reply_markup=request_enough_kb)


async def showing_request_info(message: types.Message, state: FSMContext):
    await state.set_state(CreateRequest.waiting_confirm)
    data = await state.get_data()

    template = render_template("create_request_info.j2", data=data)

    await message.answer(template)
    await message.answer("Відправити звернення?", reply_markup=yes_n_no)


async def confirm_request(message: types.Message, state: FSMContext):
    temp_message = await message.answer(
        "Відправляємо звернення", reply_markup=ReplyKeyboardRemove()
    )

    data = await state.get_data()

    request_photos = data.get("RequestImages") or []
    photos_urls = []

    for photo in request_photos:
        photos_urls.append(f"{config.WEBHOOK_ADDRESS}/media/{photo}")

    request_id = await HttpChatBot.create_request(
        CreateRequestDto(
            user_id=data.get("UserId"),
            problem_id=data.get("ProblemId"),
            reason_id=data.get("ReasonId"),
            city_id=data.get("CityId"),
            street_id=data.get("StreetId"),
            house=data.get("House"),
            flat=data.get("Flat"),
            comment=data.get("Comment"),
            show_on_site=data.get("ShowOnSite"),
            photos=photos_urls,
        )
    )

    await temp_message.delete()

    if not request_id:
        return await message.answer(
            text="Виникла помилка з запитом. Спробувати ще раз?", reply_markup=yes_n_no
        )

    await message.answer(f"Звернення №{request_id} відправлено успішно!")

    await to_main_menu_reply(message, state)


# To main cabinet handlers


async def to_main_menu_inline(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    chat_id = callback.from_user.id

    print("HEre")

    await reset_user_request_state(state, bot=bot, chat_id=chat_id)


async def to_main_menu_reply(message: types.Message, state: FSMContext):
    await reset_user_request_state(state, message=message)


async def reset_user_request_state(state: FSMContext, **kwargs):
    await give_cabinet_menu(state=state, **kwargs)

    user_data = await state.get_data()
    request_photos = user_data.get("RequestImages")

    delete_tmp_media(request_photos)

    await update_user_state_data(state)

    await state.set_state(CabinetStates.waiting_menu)


# Back handlers


async def manually_address_back(message: types.Message, state: FSMContext, bot: Bot):
    chat_id = message.chat.id
    data = await state.get_data()

    await state.set_state(CreateRequest.waiting_address)

    await bot.send_message(chat_id=chat_id, text="Підтема прийнята")

    street = data.get("Street")
    house = data.get("House")

    await bot.send_message(
        chat_id=chat_id,
        text=f"Місце де все трапилось {street} {house}?",
        reply_markup=request_yes_no_kb,
    )


async def street_back(message: types.Message, state: FSMContext):
    await state.set_state(CreateRequest.is_address_manually)

    await message.answer(
        text="Потрібно відображати цю проблему на сайті?", reply_markup=request_yes_no_kb
    )


async def flat_back(message: types.Message, state: FSMContext):
    await state.set_state(CreateRequest.waiting_reason)
    await message.answer(reply_markup=ReplyKeyboardRemove(), text="Добре")
    message = await message.answer(text=texts.ASKGING_REASON, reply_markup=pick_reason_kb)

    return await state.update_data(ReasonsMessageId=message.message_id)


async def comment_back(message: types.Message, state: FSMContext):
    await ask_flat(message, state)


async def showing_status_back(message: types.Message, state: FSMContext):
    await state.set_state(CreateRequest.waiting_comment)
    return await message.answer(
        text="Залиште коментар стосовно проблеми", reply_markup=request_comment_kb
    )


async def saving_images_back(message: types.Message, state: FSMContext):
    await state.set_state(CreateRequest.waiting_showing_status)

    await message.answer(
        text="Потрібно відображати цю проблему на сайті?", reply_markup=request_yes_no_kb
    )


# Helpers


async def delete_message(bot: Bot, chat_id: int, message_id: int):
    try:
        await bot.delete_message(chat_id, message_id)
    except Exception:
        print("Delete message error")
