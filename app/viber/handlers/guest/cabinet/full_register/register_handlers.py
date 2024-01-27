from asyncio import sleep

import texts
from handlers.common.flat import FlatHandlers
from keyboards.common import choose_gender_kb, without_flat_kb
from keyboards.register import registration_agreement_kb
from models import Gender
from states import GuestFullRegisterStates
from utils.template_engine import render_template
from viber import viber
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.types import requests, messages


async def save_phone(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    try:
        phone = request.message.contact.phone_number
    except:
        phone = request.message.text

    await state.update_data(Phone=phone)
    await viber.send_messages(
        request.sender.id,
        messages.TextMessage(text=texts.GOT_PHONE),
    )

    await sleep(0.2)

    await viber.send_message(
        request.sender.id,
        messages.KeyboardMessage(text=texts.ASKING_FLAT, keyboard=without_flat_kb),
    )

    await state.set_state(GuestFullRegisterStates.waiting_flat)


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
        new_state=GuestFullRegisterStates.waiting_first_name,
        callback=callback,
    )


async def save_first_name(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    first_name = request.message.text

    await state.update_data(FirstName=first_name)
    await state.set_state(GuestFullRegisterStates.waiting_middle_name)

    await viber.send_message(
        request.sender.id,
        messages.TextMessage(text=texts.ASKING_LAST_NAME),
    )


async def save_middle_name(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)
    middle_name = request.message.text

    await state.update_data(MiddleName=middle_name)
    await state.set_state(GuestFullRegisterStates.waiting_last_name)

    await viber.send_message(
        request.sender.id,
        messages.TextMessage(text=texts.ASKING_MIDDLE_NAME),
    )


async def save_last_name(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)
    last_name = request.message.text

    await state.update_data(LastName=last_name)
    await state.set_state(GuestFullRegisterStates.waiting_gender)

    await viber.send_message(
        request.sender.id,
        messages.KeyboardMessage(text=texts.ASKING_GENDER, keyboard=choose_gender_kb),
    )


async def save_gender(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    gender = Gender.get_key(request.message.text)
    await state.update_data(Gender=gender)
    await state.set_state(GuestFullRegisterStates.waiting_password)

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
    await state.set_state(GuestFullRegisterStates.waiting_agreement)

    return await show_agreement(request, data)


async def show_agreement(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    await viber.send_message(
        request.sender.id,
        messages.KeyboardMessage(
            text=render_template("register/agreement.j2"), keyboard=registration_agreement_kb
        ),
    )
