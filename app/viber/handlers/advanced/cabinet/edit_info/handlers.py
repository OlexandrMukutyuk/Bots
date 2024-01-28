import texts
from dto.chat_bot import UpdateUserDto
from handlers.advanced.cabinet.menu.handlers import send_edit_user_info
from handlers.common.helpers import full_cabinet_menu
from handlers.common.house import HouseHandlers
from handlers.common.streets import StreetsHandlers
from keyboards.common import back_kb, without_flat_back_kb
from keyboards.user import edit_text, change_gender_kb
from models import Gender
from services.database import update_last_message
from services.http_client import HttpChatBot
from states.advanced import FullEditInfoStates
from texts import WITHOUT_FLAT
from viber import viber
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.types import messages, requests


async def handle_buttons(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    button_type = request.message.text
    sender_id = request.sender.id

    if button_type == edit_text["first_name_text"]:
        await state.set_state(FullEditInfoStates.waiting_first_name)
        await update_last_message(sender_id, texts.ASKING_FIRST_NAME, back_kb)

        await viber.send_message(
            sender_id, messages.KeyboardMessage(text=texts.ASKING_FIRST_NAME, keyboard=back_kb)
        )
        return

    if button_type == edit_text["middle_name_text"]:
        await state.set_state(FullEditInfoStates.waiting_middle_name)
        await update_last_message(sender_id, texts.ASKING_MIDDLE_NAME, back_kb)

        await viber.send_message(
            sender_id, messages.KeyboardMessage(text=texts.ASKING_MIDDLE_NAME, keyboard=back_kb)
        )
        return

    if button_type == edit_text["last_name_text"]:
        await state.set_state(FullEditInfoStates.waiting_last_name)
        await update_last_message(sender_id, texts.ASKING_LAST_NAME, back_kb)

        await viber.send_message(
            sender_id, messages.KeyboardMessage(text=texts.ASKING_LAST_NAME, keyboard=back_kb)
        )
        return

    if button_type == edit_text["gender_text"]:
        await state.set_state(FullEditInfoStates.waiting_gender)
        await update_last_message(sender_id, texts.ASKING_GENDER, change_gender_kb)

        await viber.send_message(
            sender_id, messages.KeyboardMessage(text=texts.ASKING_GENDER, keyboard=change_gender_kb)
        )
        return

    if button_type == edit_text["street_text"]:
        await state.set_state(FullEditInfoStates.waiting_street_typing)
        await update_last_message(sender_id, texts.ASKING_STREET, back_kb)

        await viber.send_message(
            sender_id, messages.KeyboardMessage(text=texts.ASKING_STREET, keyboard=back_kb)
        )
        return

    if button_type == edit_text["house_text"]:
        await state.set_state(FullEditInfoStates.waiting_house)
        await update_last_message(sender_id, texts.ASKING_HOUSE, back_kb)

        await viber.send_message(
            sender_id, messages.KeyboardMessage(text=texts.ASKING_HOUSE, keyboard=back_kb)
        )
        return

    if button_type == edit_text["flat_text"]:
        await state.set_state(FullEditInfoStates.waiting_flat)
        await update_last_message(sender_id, texts.ASKING_FLAT, without_flat_back_kb)

        await viber.send_message(
            sender_id,
            messages.KeyboardMessage(text=texts.ASKING_FLAT, keyboard=without_flat_back_kb),
        )
        return


async def edit_first_name(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    first_name = request.message.text

    await state.update_data(FirstName=first_name)
    await state.set_state(FullEditInfoStates.waiting_acceptation)

    await send_edit_user_info(request, data)


async def edit_middle_name(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    middle_name = request.message.text

    await state.update_data(MiddleName=middle_name)
    await state.set_state(FullEditInfoStates.waiting_acceptation)

    await send_edit_user_info(request, data)


async def edit_last_name(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    last_name = request.message.text

    await state.update_data(LastName=last_name)
    await state.set_state(FullEditInfoStates.waiting_acceptation)

    await send_edit_user_info(request, data)


# Edit other


async def edit_street(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    return await StreetsHandlers.choose_street(
        request=request, state=state, new_state=FullEditInfoStates.waiting_street_selected
    )


async def confirm_street(request: requests.ViberMessageRequest, data: dict):
    text_list = request.message.text.split(":")

    street_id = int(text_list[1])
    city_id = int(text_list[2])

    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    async def action():
        await state.set_state(FullEditInfoStates.waiting_acceptation)
        await send_edit_user_info(request, data)

    return await StreetsHandlers.confirm_street(
        street_id=street_id, city_id=city_id, state=state, action=action
    )


async def edit_house(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    async def callback():
        await send_edit_user_info(request, data)

    return await HouseHandlers.change_house(
        request=request,
        state=state,
        new_state=FullEditInfoStates.waiting_acceptation,
        callback=callback,
    )


async def edit_flat(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    flat = request.message.text

    if flat == WITHOUT_FLAT:
        flat = None

    await state.update_data(Flat=flat)
    await state.set_state(FullEditInfoStates.waiting_acceptation)

    await send_edit_user_info(request, data)


async def edit_gender(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    gender = Gender.get_key(request.message.text)

    await state.update_data(Gender=gender)
    await state.set_state(FullEditInfoStates.waiting_acceptation)

    await send_edit_user_info(request, data)


async def confirm(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)
    user_data = await state.get_data()

    await HttpChatBot.update_profile(
        UpdateUserDto(
            user_id=user_data.get("UserId"),
            phone=user_data.get("Phone"),
            city_id=user_data.get("CityId"),
            street_id=user_data.get("StreetId"),
            house=user_data.get("House"),
            flat=user_data.get("Flat"),
            first_name=user_data.get("FirstName"),
            middle_name=user_data.get("MiddleName"),
            last_name=user_data.get("LastName"),
            gender=user_data.get("Gender"),
        )
    )

    await viber.send_message(
        request.sender.id, messages.TextMessage(text=texts.EDITED_SUCCESSFULLY)
    )

    return await full_cabinet_menu(request, data)


# Validation


async def not_valid_flat(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    flat = request.message.text

    await state.update_data(Flat=flat)
    await state.set_state(FullEditInfoStates.waiting_acceptation)

    await send_edit_user_info(request, data)
