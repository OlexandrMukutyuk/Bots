import os

import texts
from data import config
from dto.chat_bot import UserIdDto, ProblemIdDto, CreateRequestDto, AddressByGeoDto
from handlers.common.flat import FlatHandlers
from handlers.common.helpers import full_cabinet_menu, update_user_state_data
from handlers.common.house import HouseHandlers
from handlers.common.streets import StreetsHandlers
from keyboards.common import yes_n_no
from keyboards.create_request import (
    generate_reasons_kb,
    request_yes_no_kb,
    request_manual_address_kb,
    request_back_and_main_kb,
    request_house_kb,
    request_flat_kb,
    request_comment_kb,
    request_images_kb,
    request_enough_kb,
)
from services.database import update_last_message
from services.http_client import HttpChatBot, download_image
from states.advanced import CreateRequestStates
from texts import BACK, YES, NO_NEED, ENOUGH
from utils.media import delete_tmp_media, get_filename_from_url
from utils.template_engine import render_template
from viber import viber
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.types import requests, messages


async def confirm_problem(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)
    data = await state.get_data()

    sender_id = request.sender.id

    text_list = request.message.text.split(":")
    problem_id = int(text_list[1])

    problems = await HttpChatBot.get_problems(UserIdDto(user_id=data.get("UserId")))
    problem_name = ""

    for problem in problems:
        if problem.get("Id") == problem_id:
            problem_name = problem.get("Name")

    await state.set_state(CreateRequestStates.waiting_reason)

    await viber.send_message(
        sender_id,
        messages.TextMessage(text="Тема прийнята. Завантажуємо підтеми..."),
    )

    reasons = await HttpChatBot.get_reasons(ProblemIdDto(problem_id=problem_id))

    kb = generate_reasons_kb(reasons)

    await update_last_message(sender_id, texts.ASKING_REASON, kb)

    await viber.send_message(
        sender_id,
        messages.KeyboardMessage(text=texts.ASKING_REASON, keyboard=kb),
    )

    await state.set_data(
        {
            **data,
            "Reasons": reasons,
            "ProblemId": problem_id,
            "ProblemName": problem_name,
        }
    )


async def confirm_reason(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    sender_id = request.sender.id

    text_list = request.message.text.split(":")
    reason_id = int(text_list[1])

    data = await state.get_data()

    reasons = await HttpChatBot.get_reasons(ProblemIdDto(problem_id=data.get("ProblemId")))
    reason_name = ""

    for reason in reasons:
        if reason.get("Id") == reason_id:
            reason_name = reason.get("Name")

    await state.set_state(CreateRequestStates.waiting_address)
    await state.set_data({"ReasonId": reason_id, "ReasonName": reason_name, **data})

    await viber.send_message(
        sender_id,
        messages.TextMessage(text="Підтема прийнята"),
    )

    street = data.get("Street")
    house = data.get("House")

    address_text = f"Місце де все трапилось {street} {house}?"

    await update_last_message(sender_id, address_text, request_yes_no_kb)

    await viber.send_message(
        sender_id,
        messages.TextMessage(text=address_text, keyboard=request_yes_no_kb),
    )


async def request_on_my_site(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)
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

    return await ask_flat(request, data)


async def manually_type_location(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    sender_id = request.sender.id

    await state.set_state(CreateRequestStates.is_address_manually)

    address_text = (
        "Ви можете поділитися геолокацією, або вписати адресу вручну. Передача гео не працює з ПК."
    )

    await update_last_message(sender_id, address_text, request_manual_address_kb)

    await viber.send_message(
        sender_id,
        messages.KeyboardMessage(
            text=address_text,
            keyboard=request_manual_address_kb,
            min_api_version="3",
        ),
    )


async def location_by_geo(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)
    user_data = await state.get_data()
    sender_id = request.sender.id

    lat = request.message.location.lat
    lng = request.message.location.lon
    user_id = user_data.get("UserId")

    address_info = await HttpChatBot.get_address_by_geo(
        AddressByGeoDto(user_id=user_id, lat=lat, lng=lng)
    )

    if not address_info:
        await viber.send_message(
            sender_id,
            messages.TextMessage(
                text="Виникла помилка з запитом. Спробувати ще раз?", keyboard=yes_n_no
            ),
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

    return await ask_flat(request, data)


async def ask_for_street_name(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    sender_id = request.sender.id
    await update_last_message(sender_id, texts.ASKING_STREET, request_back_and_main_kb)

    await state.set_state(CreateRequestStates.waiting_street_typing)
    await viber.send_message(
        sender_id,
        messages.KeyboardMessage(
            text=texts.ASKING_STREET,
            keyboard=request_back_and_main_kb,
        ),
    )


async def type_street(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    return await StreetsHandlers.choose_street(
        request=request, state=state, new_state=CreateRequestStates.waiting_street_selected
    )


async def confirm_street(request: requests.ViberMessageRequest, data: dict):
    text_list = request.message.text.split(":")

    street_id = int(text_list[1])
    city_id = int(text_list[2])

    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    async def action():
        await state.set_state(CreateRequestStates.waiting_house)

        sender_id = request.sender.id
        await update_last_message(sender_id, texts.ASKING_HOUSE, request_house_kb)

        await viber.send_message(
            sender_id,
            messages.KeyboardMessage(text=texts.ASKING_HOUSE, keyboard=request_house_kb),
        )

    return await StreetsHandlers.confirm_street(
        street_id=street_id, city_id=city_id, state=state, action=action
    )


async def change_street(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    await state.set_state(CreateRequestStates.waiting_street_typing)

    sender_id = request.sender.id
    await update_last_message(sender_id, texts.ASKING_STREET)

    await viber.send_message(
        sender_id,
        messages.TextMessage(text=texts.ASKING_STREET),
    )


async def save_house(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    async def callback():
        return await ask_flat(request, data)

    await HouseHandlers.change_house(
        request=request,
        state=state,
        new_state=CreateRequestStates.waiting_flat,
        callback=callback,
    )


async def ask_flat(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    await state.set_state(CreateRequestStates.waiting_flat)

    sender_id = request.sender.id
    await update_last_message(sender_id, texts.ASKING_FLAT, request_flat_kb)

    await viber.send_message(
        sender_id,
        messages.KeyboardMessage(text=texts.ASKING_FLAT, keyboard=request_flat_kb),
    )


async def save_flat(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    async def callback():
        sender_id = request.sender.id

        text = "Залиште коментар стосовно проблеми"
        await update_last_message(sender_id, text, request_comment_kb)

        await viber.send_message(
            sender_id,
            messages.KeyboardMessage(text=text, keyboard=request_comment_kb),
        )

    await FlatHandlers.change_flat(
        request=request,
        state=state,
        new_state=CreateRequestStates.waiting_comment,
        callback=callback,
    )


async def save_comment(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)
    text = request.message.text

    if text == BACK:
        return await ask_flat(request, data)

    await state.update_data(Comment=text)

    sender_id = request.sender.id

    text = "Потрібно відображати цю проблему на сайті?"
    await update_last_message(sender_id, text, request_yes_no_kb)

    await viber.send_message(
        sender_id,
        messages.KeyboardMessage(text=text, keyboard=request_yes_no_kb),
    )

    await state.set_state(CreateRequestStates.waiting_showing_status)


async def save_showing_status(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)
    text = request.message.text

    if text == YES:
        show_on_site = True
    else:
        show_on_site = False

    await state.update_data(ShowOnSite=show_on_site)

    sender_id = request.sender.id

    text = "Прикріпляйте фото якщо необхідно"

    await viber.send_message(
        sender_id,
        messages.TextMessage(text=text),
    )

    await viber.send_message(
        sender_id,
        messages.KeyboardMessage(text="Тільки по одному", keyboard=request_images_kb),
    )

    await update_last_message(sender_id, text, request_images_kb)

    await state.set_state(CreateRequestStates.waiting_images)


async def saving_images(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    text = request.message.text
    if text in [NO_NEED, ENOUGH]:
        return await showing_request_info(request, data)

    media_url = request.message.media
    file_name = get_filename_from_url(media_url)

    data = await state.get_data()

    images = data.get("RequestImages") or []

    await state.update_data(RequestImages=[*images, file_name])

    await download_image(media_url, f"{os.getcwd()}/media/{file_name}")

    sender_id = request.sender.id

    await viber.send_message(
        sender_id,
        messages.KeyboardMessage(text="Завантажуйте ще", keyboard=request_enough_kb),
    )

    await update_last_message(sender_id, "Завантажуйте ще", request_enough_kb)


async def showing_request_info(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)
    data = await state.get_data()

    await state.set_state(CreateRequestStates.waiting_confirm)

    template = render_template("create_request_info.j2", data=data)

    sender_id = request.sender.id

    await update_last_message(sender_id, "Відправити звернення?", yes_n_no)

    await viber.send_message(
        sender_id,
        messages.TextMessage(text=template),
    )

    await viber.send_message(
        sender_id,
        messages.KeyboardMessage(text="Відправити звернення?", keyboard=yes_n_no),
    )


async def confirm_request(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    sender_id = request.sender.id
    await viber.send_message(
        sender_id,
        messages.TextMessage(text="Відправляємо звернення"),
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

    if not request_id:

        error = "Виникла помилка з запитом. Спробувати ще раз?"
        await update_last_message(sender_id, error, yes_n_no)

        return await viber.send_message(
            sender_id,
            messages.KeyboardMessage(
                text=error, keyboard=yes_n_no
            ),
        )

    await viber.send_message(
        sender_id,
        messages.TextMessage(text=f"Звернення №{request_id} відправлено успішно!"),
    )

    await reset_user_request_state(request, data)


async def reset_user_request_state(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    user_data = await state.get_data()
    request_photos = user_data.get("RequestImages")

    delete_tmp_media(request_photos)

    await update_user_state_data(state)

    await full_cabinet_menu(request, data)


# Back handlers


async def manually_address_back(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)
    await state.set_state(CreateRequestStates.waiting_reason)

    reasons = (await state.get_data()).get("Reasons")

    sender_id = request.sender.id
    kb = generate_reasons_kb(reasons)

    await update_last_message(sender_id, texts.ASKING_REASON, kb)


    await viber.send_message(
        sender_id,
        messages.KeyboardMessage(text=texts.ASKING_REASON, keyboard=kb),
    )



async def flat_back(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)
    data = await state.get_data()

    sender_id = request.sender.id

    await state.set_state(CreateRequestStates.waiting_address)

    await viber.send_message(
        sender_id,
        messages.TextMessage(text="Підтема прийнята"),
    )

    street = data.get("Street")
    house = data.get("House")

    sender_id = request.sender.id

    text = f"Місце де все трапилось {street} {house}?"

    await update_last_message(sender_id, text, request_yes_no_kb)


    await viber.send_message(
        sender_id,
        messages.KeyboardMessage(
            text=text, keyboard=request_yes_no_kb
        ),
    )


async def showing_status_back(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)
    await state.set_state(CreateRequestStates.waiting_comment)

    sender_id = request.sender.id

    await update_last_message(sender_id, "Залиште коментар стосовно проблеми", request_comment_kb)


    await viber.send_message(
        sender_id,
        messages.KeyboardMessage(
            text="Залиште коментар стосовно проблеми", keyboard=request_comment_kb
        ),
    )


async def saving_images_back(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)
    await state.set_state(CreateRequestStates.waiting_showing_status)

    sender_id = request.sender.id

    await update_last_message(sender_id, "Потрібно відображати цю проблему на сайті?", request_yes_no_kb)


    await viber.send_message(
        sender_id,
        messages.KeyboardMessage(
            text="Потрібно відображати цю проблему на сайті?", keyboard=request_yes_no_kb
        ),
    )

