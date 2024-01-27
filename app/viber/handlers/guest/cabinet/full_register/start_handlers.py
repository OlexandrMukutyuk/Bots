from asyncio import sleep

import texts
from data.config import WEBSITE_URL
from handlers.common.email import EmailHandlers
from keyboards.common import yes_n_no
from keyboards.register import phone_share_kb
from keyboards.start import start_again_kb, is_register_on_site
from states import GuestFullRegisterStates
from texts import YES, NO
from utils.template_engine import render_template
from viber import viber
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.types import requests, messages


async def asking_email(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    await viber.send_message(
        request.sender.id,
        messages.TextMessage(text=texts.ASKING_EMAIL),
    )

    await state.set_state(GuestFullRegisterStates.waiting_email)


async def check_user_email(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    async def action():
        return await asking_if_register(request, data)

    await EmailHandlers.check_user(
        request=request,
        state=state,
        exist_state=GuestFullRegisterStates.waiting_code,
        action=action,
    )


async def check_email_code(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    async def action():
        return await start_again(request, data)

    await EmailHandlers.check_code(
        request=request,
        state=state,
        failure_state=GuestFullRegisterStates.waiting_code,
        other_email_action=action,
    )


async def answer_if_register(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    message_text = request.message.text

    if message_text == YES:
        await asking_if_email_confirmed(request, data)

    if message_text == NO:
        await viber.send_messages(
            request.sender.id,
            [
                messages.TextMessage(text=texts.NEED_REGISTER),
                messages.TextMessage(text=texts.ASKING_PHONE),
            ],
        )

        await sleep(0.2)
        await viber.send_message(
            request.sender.id,
            messages.KeyboardMessage(text=texts.PHONE_EXAMPLE, keyboard=phone_share_kb, min_api_version='3'),
        )
        await state.set_state(GuestFullRegisterStates.waiting_phone)


async def answer_if_confirmed_email(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    message_text = request.message.text

    if message_text == YES:
        await viber.send_messages(
            request.sender.id,
            messages.KeyboardMessage(text=texts.CALL_SUPPORT, keyboard=start_again_kb),
        )

    if message_text == NO:
        await viber.send_messages(
            request.sender.id,
            messages.KeyboardMessage(
                text=render_template("website_link.j2", url=WEBSITE_URL), keyboard=start_again_kb
            ),
        )


async def start_again(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    await state.update_data(Email=None)

    await asking_email(request, data)


async def asking_if_register(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    await viber.send_message(
        request.sender.id,
        messages.KeyboardMessage(text=texts.IS_REGISTER_ON_SITE, keyboard=is_register_on_site),
    )
    await state.set_state(GuestFullRegisterStates.answering_if_register)


async def asking_if_email_confirmed(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    await state.set_state(GuestFullRegisterStates.answering_if_confirmed_email)
    await viber.send_message(
        request.sender.id,
        messages.KeyboardMessage(text=texts.IS_REGISTER_ON_SITE, keyboard=yes_n_no),
    )
