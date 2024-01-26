import texts
from data.config import WEBSITE_URL
from handlers.common.email import EmailHandlers
from keyboards.common import yes_n_no
from keyboards.register import phone_share_kb
from keyboards.start import greeting_kb, auth_types_kb, start_again_kb, is_register_on_site, big_kb
from states import StartState, AuthState, GuestAuthStates, LoginState, AdvancedRegisterStates
from texts import YES, NO
from utils.template_engine import render_template
from viber import viber
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.types import messages, requests


async def test(req: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(req)

    text = messages.KeyboardMessage(text=texts.SERVER_ERROR, keyboard=big_kb)

    return await viber.send_message(req.sender.id, text)


async def greeting(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    await state.clear()
    await state.set_state(StartState.waiting_greeting)

    text = messages.KeyboardMessage(text=texts.GREETING, keyboard=greeting_kb, min_api_version="4")

    return await viber.send_message(request.sender.id, text)


async def introduction(request: requests.ViberMessageRequest, data: dict):
    chat_id = request.sender.id

    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)
    await state.set_state(StartState.waiting_auth_type)

    await viber.send_messages(
        chat_id,
        [
            messages.TextMessage(text=texts.INTRODUCTION),
            messages.TextMessage(text=texts.PICK_AUTH_TYPE),
            messages.KeyboardMessage(
                text=texts.ADVANCED_INFO, keyboard=auth_types_kb, min_api_version="4"
            ),
            messages.KeyboardMessage(
                text=texts.SUBSCRIPTION_INFO, keyboard=auth_types_kb, min_api_version="4"
            ),
        ],
    )


async def check_user_email(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    async def action():
        return await asking_if_register(request, data)

    await EmailHandlers.check_user(
        req=request, state=state, exist_state=LoginState.waiting_code, action=action
    )


async def answer_if_register(request: requests.ViberMessageRequest, data: dict):
    message_text = request.message.text

    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    if message_text == YES:
        await asking_if_email_confirmed(request, data)

    if message_text == NO:
        await viber.send_messages(
            request.sender.id,
            [
                messages.TextMessage(text=texts.NEED_REGISTER),
                messages.TextMessage(text=texts.ASKING_PHONE),
                messages.KeyboardMessage(
                    text=texts.PHONE_EXAMPLE, keyboard=phone_share_kb, min_api_version="4"
                ),
            ],
        )
        await state.set_state(AdvancedRegisterStates.waiting_phone)


async def answer_if_confirmed_email(request: requests.ViberMessageRequest, data: dict):
    message_text = request.message.text

    if message_text == YES:
        await viber.send_message(
            request.sender.id,
            messages.KeyboardMessage(text=texts.NEED_REGISTER, keyboard=start_again_kb),
        )

    if message_text == NO:
        await viber.send_message(
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


async def asking_email(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)
    await state.set_state(StartState.waiting_greeting)

    await viber.send_message(
        request.sender.id,
        messages.TextMessage(text=texts.ASKING_EMAIL),
    )
    await state.set_state(AuthState.waiting_email)


async def asking_if_register(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    await state.set_state(AuthState.answering_if_register)

    await viber.send_message(
        request.sender.id,
        messages.KeyboardMessage(text=texts.IS_REGISTER_ON_SITE, keyboard=is_register_on_site),
    )


async def asking_if_email_confirmed(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    await state.set_state(AuthState.answering_if_confirmed_email)

    await viber.send_message(
        request.sender.id,
        messages.KeyboardMessage(text=texts.IS_EMAIL_CONFIRMED, keyboard=yes_n_no),
    )


async def subscription_auth(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    await state.set_state(GuestAuthStates.waiting_street_typing)

    await viber.send_message(request.sender.id, messages.TextMessage(text=texts.ASKING_STREET))
