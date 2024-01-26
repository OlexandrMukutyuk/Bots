import texts
from bot import viber
from keyboards.common import back_kb, choose_gender_kb
from viberio.types import requests, messages


async def not_valid_email(request: requests.ViberMessageRequest, data: dict):
    await viber.send_message(request.sender.id, messages.TextMessage(text=texts.NOT_VALID_EMAIL))
    await viber.send_message(request.sender.id, messages.TextMessage(text=texts.ASKING_EMAIL))


async def not_valid_phone(request: requests.ViberMessageRequest, data: dict):
    await viber.send_message(request.sender.id, messages.TextMessage(text=texts.NOT_VALID_PHONE))


async def not_valid_street_name(request: requests.ViberMessageRequest, data: dict):
    await viber.send_message(
        request.sender.id, messages.TextMessage(text=texts.NOT_VALID_STREET_NAME)
    )
    await viber.send_message(request.sender.id, messages.TextMessage(text=texts.TRY_AGAIN))


async def not_valid_flat(request: requests.ViberMessageRequest, data: dict):
    await viber.send_message(request.sender.id, messages.TextMessage(text=texts.NOT_VALID_FLAT))
    await viber.send_message(request.sender.id, messages.TextMessage(text=texts.ASKING_FLAT))


async def not_valid_gender(request: requests.ViberMessageRequest, data: dict):
    await viber.send_message(
        request.sender.id, messages.TextMessage(text="Ви ввели недопустиме значення")
    )
    await viber.send_message(
        request.sender.id,
        messages.KeyboardMessage(text=texts.ASKING_GENDER, keyboard=choose_gender_kb),
    )


async def weak_password(request: requests.ViberMessageRequest, data: dict):
    await viber.send_message(request.sender.id, messages.TextMessage(text=texts.WEAK_PASSWORD))
    await viber.send_message(request.sender.id, messages.TextMessage(text=texts.ASKING_PASSWORD))
    await viber.send_message(request.sender.id, messages.TextMessage(text=texts.PASSWORD_REQS))


async def not_valid_first_name(request: requests.ViberMessageRequest, data: dict):
    await viber.send_message(request.sender.id, messages.TextMessage(text=texts.NOT_VALID_NAME))
    await viber.send_message(request.sender.id, messages.TextMessage(text=texts.ASKING_FIRST_NAME))


async def not_valid_last_name(request: requests.ViberMessageRequest, data: dict):
    await viber.send_message(request.sender.id, messages.TextMessage(text=texts.NOT_VALID_NAME))
    await viber.send_message(request.sender.id, messages.TextMessage(text=texts.ASKING_LAST_NAME))


async def not_valid_middle_name(request: requests.ViberMessageRequest, data: dict):
    await viber.send_message(request.sender.id, messages.TextMessage(text=texts.NOT_VALID_NAME))
    await viber.send_message(request.sender.id, messages.TextMessage(text=texts.ASKING_MIDDLE_NAME))


async def not_valid_text(request: requests.ViberMessageRequest, data: dict):
    await viber.send_message(request.sender.id, messages.TextMessage(text=texts.NOT_VALID_TEXT))


async def not_valid_text_with_back(request: requests.ViberMessageRequest, data: dict):
    await viber.send_message(
        request.sender.id, messages.TextMessage(text=texts.NOT_VALID_TEXT, keyboard=back_kb)
    )


async def not_valid_comment(request: requests.ViberMessageRequest, data: dict):
    await viber.send_message(request.sender.id, messages.TextMessage(text=texts.NOT_VALID_COMMENT))
    await viber.send_message(
        request.sender.id, messages.TextMessage(text=texts.ASKING_MIN_10_CHARS)
    )
