from typing import Callable

import texts
from dto.chat_bot import EmailDto, CheckEmailDto
from handlers.common.helpers import update_user_state_data, full_cabinet_menu
from keyboards.login import other_email_kb
from services.http_client import HttpChatBot
from viber import viber
from viberio.fsm.context import FSMContext
from viberio.fsm.states import State
from viberio.types import messages, requests


class EmailHandlers:
    @staticmethod
    async def check_user(
        req: requests.ViberMessageRequest, state: FSMContext, exist_state: State, action: Callable
    ):
        email = req.message.text
        sender_id = req.sender.id

        await state.update_data(Email=email)

        is_user_exist = await HttpChatBot.check_email(CheckEmailDto(email=email))

        if is_user_exist:
            return await EmailHandlers.perform_sending_code(
                sender_id=sender_id,
                state=state,
                email=email,
                new_state=exist_state,
            )

        await action()

    @staticmethod
    async def perform_sending_code(sender_id, state: FSMContext, email: str, new_state: State):
        data = await HttpChatBot.code_to_email(EmailDto(email=email))

        await state.update_data(EmailCode=data.get("Code"))
        await state.update_data(UserId=data.get("UserId"))

        await viber.send_messages(
            sender_id, messages.KeyboardMessage(text=texts.ASKING_CODE, keyboard=other_email_kb)
        )

        return await state.set_state(new_state)

    @staticmethod
    async def check_code(
        request: requests.ViberMessageRequest,
        state: FSMContext,
        failure_state: State,
        other_email_action: Callable,
    ):
        data = await state.get_data()
        correct_code = data.get("EmailCode")

        user_text = request.message.text
        sender_id = request.sender.id

        if user_text == texts.OTHER_MAIL:
            return await other_email_action()

        email = data.get("Email")

        if correct_code != user_text:
            await viber.send_messages(sender_id, messages.TextMessage(text=texts.WRONG_CODE))
            await EmailHandlers.perform_sending_code(
                sender_id=sender_id, state=state, email=email, new_state=failure_state
            )
            return

        await viber.send_messages(sender_id, messages.TextMessage(text=texts.SUCCESSFUL_AUTH))

        await update_user_state_data(state)
        await full_cabinet_menu(request, data)
