import texts
from handlers.common.flat import FlatHandlers
from handlers.common.house import HouseHandlers
from handlers.common.streets import StreetsHandlers
from keyboards.common import without_flat_kb, choose_gender_kb
from keyboards.register import registration_agreement_kb
from keyboards.streets import change_street_kb
from models import Gender
from states import AdvancedRegisterStates
from utils.template_engine import render_template
from viber import viber
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.types import requests, messages


async def save_phone(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    phone = request.message.contact.phone_number or request.message.text

    await state.update_data(Phone=phone)
    await viber.send_messages(
        request.sender.id,
        [
            messages.TextMessage(text="Ваш номер успішно відправлено"),
            messages.TextMessage(text=texts.ASKING_STREET),
        ],
    )

    await state.set_state(AdvancedRegisterStates.waiting_street_typing)


async def choose_street(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    return await StreetsHandlers.choose_street(
        request=request, state=state, new_state=AdvancedRegisterStates.waiting_street_selected
    )


async def confirm_street(request: requests.ViberMessageRequest, data: dict):
    text_list = request.message.text.split(":")

    street_id = int(text_list[1])
    city_id = int(text_list[2])

    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    async def action():
        await state.set_state(AdvancedRegisterStates.waiting_house)

        await viber.send_message(
            request.sender.id,
            messages.KeyboardMessage(text=texts.ASKING_HOUSE, keyboard=change_street_kb),
        )

    return await StreetsHandlers.confirm_street(
        street_id=street_id, city_id=city_id, state=state, action=action
    )


async def change_street(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    await state.set_state(AdvancedRegisterStates.waiting_street_typing)

    await viber.send_message(
        request.sender.id,
        messages.TextMessage(text=texts.ASKING_STREET),
    )


async def save_house(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    async def callback():
        await viber.send_message(
            request.sender.id,
            messages.KeyboardMessage(text=texts.ASKING_FLAT, keyboard=without_flat_kb),
        )

    await HouseHandlers.change_house(
        request=request,
        state=state,
        new_state=AdvancedRegisterStates.waiting_flat,
        callback=callback,
    )


async def save_flat(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    async def callback():
        await viber.send_message(
            request.sender.id,
            messages.TextMessage(text=texts.ASKING_FIRST_NAME),
        )

    return await FlatHandlers.change_flat(
        request=request,
        state=state,
        new_state=AdvancedRegisterStates.waiting_first_name,
        callback=callback,
    )


async def save_first_name(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    first_name = request.message.text

    await state.update_data(FirstName=first_name)
    await state.set_state(AdvancedRegisterStates.waiting_middle_name)

    await viber.send_message(
        request.sender.id,
        messages.TextMessage(text=texts.ASKING_MIDDLE_NAME),
    )


async def save_middle_name(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    middle_name = request.message.text

    await state.update_data(MiddleName=middle_name)
    await state.set_state(AdvancedRegisterStates.waiting_last_name)

    await viber.send_message(
        request.sender.id,
        messages.TextMessage(text=texts.ASKING_LAST_NAME),
    )


async def save_last_name(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    last_name = request.message.text

    await state.update_data(LastName=last_name)
    await state.set_state(AdvancedRegisterStates.waiting_gender)

    await viber.send_message(
        request.sender.id,
        messages.KeyboardMessage(
            text=texts.ASKING_GENDER, keyboard=choose_gender_kb, min_api_version="4"
        ),
    )


async def save_gender(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    gender = Gender.get_key(request.message.text)
    await state.update_data(Gender=gender)
    await state.set_state(AdvancedRegisterStates.waiting_password)

    await viber.send_messages(
        request.sender.id,
        [
            messages.TextMessage(text=texts.ASKING_PASSWORD),
            messages.TextMessage(text=texts.PASSWORD_REQS),
        ],
    )


async def save_password(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    await state.update_data(Password=request.message.text)
    await state.set_state(AdvancedRegisterStates.waiting_agreement)

    return await show_agreement(request, data)


async def show_agreement(request: requests.ViberMessageRequest, data: dict):
    await viber.send_message(
        request.sender.id,
        messages.KeyboardMessage(
            text=render_template("register/agreement.j2"), keyboard=registration_agreement_kb
        ),
    )
