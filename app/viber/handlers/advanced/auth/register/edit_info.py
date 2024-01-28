import texts
from dto.chat_bot import RegisterDto
from handlers.common.flat import FlatHandlers
from handlers.common.house import HouseHandlers
from handlers.common.streets import StreetsHandlers
from keyboards.login import other_email_kb
from keyboards.register import edit_register_info_kb, edit_text, phone_share_kb
from services.database import DB, update_last_message
from services.http_client import HttpChatBot
from states import EditRegisterStates
from utils.template_engine import render_template
from viber import viber
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.types import requests, messages


async def handle_buttons(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    sender_id = request.sender.id
    button_type = request.message.text

    if button_type == edit_text["first_name_text"]:
        await state.set_state(EditRegisterStates.waiting_first_name)
        await update_last_message(sender_id, texts.ASKING_FIRST_NAME)
        return await viber.send_message(
            sender_id,
            messages.TextMessage(text=texts.ASKING_FIRST_NAME),
        )

    if button_type == edit_text["middle_name_text"]:
        await state.set_state(EditRegisterStates.waiting_middle_name)
        await update_last_message(sender_id, texts.ASKING_MIDDLE_NAME)

        return await viber.send_message(
            sender_id,
            messages.TextMessage(text=texts.ASKING_MIDDLE_NAME),
        )

    if button_type == edit_text["last_name_text"]:
        await state.set_state(EditRegisterStates.waiting_last_name)
        await update_last_message(sender_id, texts.ASKING_LAST_NAME)

        return await viber.send_message(
            sender_id,
            messages.TextMessage(text=texts.ASKING_LAST_NAME),
        )

    if button_type == edit_text["phone_text"]:
        await state.set_state(EditRegisterStates.waiting_phone)
        await update_last_message(sender_id, texts.ASKING_PHONE, phone_share_kb)

        return await viber.send_messages(
            sender_id,
            [
                messages.TextMessage(text=texts.ASKING_PHONE),
                messages.KeyboardMessage(
                    text=texts.PHONE_EXAMPLE, keyboard=phone_share_kb, min_api_version="4"
                ),
            ],
        )

    if button_type == edit_text["password_text"]:
        await state.set_state(EditRegisterStates.waiting_password)
        await update_last_message(sender_id, texts.ASKING_PASSWORD)

        return await viber.send_messages(
            sender_id,
            [
                messages.TextMessage(text=texts.ASKING_PASSWORD),
                messages.TextMessage(text=texts.PASSWORD_REQS),
            ],
        )

    if button_type == edit_text["street_text"]:
        await state.set_state(EditRegisterStates.waiting_street_typing)
        await update_last_message(sender_id, texts.ASKING_STREET)

        return await viber.send_message(
            sender_id,
            messages.TextMessage(text=texts.ASKING_STREET),
        )

    if button_type == edit_text["house_text"]:
        await state.set_state(EditRegisterStates.waiting_house)
        await update_last_message(sender_id, texts.ASKING_HOUSE)

        return await viber.send_message(
            sender_id,
            messages.TextMessage(text=texts.ASKING_HOUSE),
        )

    if button_type == edit_text["flat_text"]:
        await state.set_state(EditRegisterStates.waiting_flat)
        await update_last_message(sender_id, texts.ASKING_FLAT)

        return await viber.send_message(
            sender_id,
            messages.TextMessage(text=texts.ASKING_FLAT),
        )

    if button_type == edit_text["accept_info_text"]:
        return await accept_info(request, data)


async def send_user_info(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    user_data = await state.get_data()

    await state.set_state(EditRegisterStates.waiting_accepting)

    info_template = render_template("register/confirming_info.j2", data=user_data)

    sender_id = request.sender.id
    await update_last_message(sender_id, info_template, edit_register_info_kb)

    await viber.send_messages(
        sender_id,
        [
            messages.TextMessage(text=info_template),
            messages.KeyboardMessage(
                text=texts.IS_EVERYTHING_CORRECT,
                keyboard=edit_register_info_kb,
                min_api_version="4",
            ),
        ],
    )


async def edit_phone(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    try:
        phone = request.message.contact.phone_number
    except:
        phone = request.message.text

    await state.update_data(Phone=phone)
    await state.set_state(EditRegisterStates.waiting_accepting)

    await send_user_info(request, data)


async def edit_street(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    return await StreetsHandlers.choose_street(
        request=request, state=state, new_state=EditRegisterStates.waiting_street_selected
    )


async def confirm_street(request: requests.ViberMessageRequest, data: dict):
    text_list = request.message.text.split(":")

    street_id = int(text_list[1])
    city_id = int(text_list[2])

    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    async def action():
        await state.set_state(EditRegisterStates.waiting_house)

        sender_id = request.sender.id
        await update_last_message(sender_id, texts.ASKING_HOUSE)

        await viber.send_message(
            sender_id,
            messages.TextMessage(text=texts.ASKING_HOUSE),
        )

    return await StreetsHandlers.confirm_street(
        street_id=street_id, city_id=city_id, state=state, action=action
    )


async def edit_house(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    async def callback():
        await send_user_info(request, data)

    await HouseHandlers.change_house(
        request=request,
        state=state,
        new_state=EditRegisterStates.waiting_flat,
        callback=callback,
    )


async def save_flat(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    async def callback():
        await send_user_info(request, data)

    return await FlatHandlers.change_flat(
        request=request,
        state=state,
        new_state=EditRegisterStates.waiting_first_name,
        callback=callback,
    )


async def save_first_name(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    await state.update_data(FirstName=request.message.text)
    await send_user_info(request, data)


async def save_middle_name(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    await state.update_data(MiddleName=request.message.text)
    await send_user_info(request, data)


async def save_last_name(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    await state.update_data(LastName=request.message.text)
    await send_user_info(request, data)


async def edit_password(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    await state.update_data(Password=request.message.text)

    await send_user_info(request, data)


async def accept_info(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    data = await state.get_data()

    user_id = await HttpChatBot.register(
        RegisterDto(
            first_name=data.get("FirstName"),
            last_name=data.get("LastName"),
            middle_name=data.get("MiddleName"),
            gender=data.get("Gender"),
            phone=data.get("Phone"),
            city_id=data.get("CityId"),
            street_id=data.get("StreetId"),
            house=data.get("House"),
            flat=data.get("Flat"),
            password=data.get("Password"),
            email=data.get("Email"),
        )
    )

    sender_id = request.sender.id

    await DB.update("""UPDATE users SET user_id = ? WHERE sender_id = ?""", (user_id, sender_id))

    await state.update_data(UserId=user_id)

    await state.set_state(EditRegisterStates.waiting_email_confirming)

    check_email_text = (
        "Будь ласка, підтвердіть свою пошту (перейдіть за посиланням, яке ми вам відправили)"
    )

    await viber.send_messages(
        sender_id,
        [
            messages.TextMessage(text="Інформація для реєстрації відправлена успішно!"),
            messages.TextMessage(text=check_email_text),
            messages.KeyboardMessage(
                text="Якщо лист не отримано - перевірте спам.",
                keyboard=other_email_kb,
                min_api_version="4",
            ),
        ],
    )

    await update_last_message(sender_id, check_email_text)
