from typing import Callable

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

import texts
from dto.chat_bot import EmailDto, CheckEmailDto
from handlers.common.helpers import send_loading_message, update_user_state_data, full_cabinet_menu
from keyboards.default.auth.login import other_email_kb
from services.http_client import HttpChatBot


class EmailHandlers:
    @staticmethod
    async def check_user(
        message: types.Message, state: FSMContext, exist_state: State, action: Callable
    ):
        email = message.text

        await state.update_data(Email=email)

        loading = await send_loading_message(message=message)

        is_user_exist = await HttpChatBot.check_email(CheckEmailDto(email=email))

        await loading.delete()

        if is_user_exist:
            return await EmailHandlers.perform_sending_code(
                message=message,
                state=state,
                email=email,
                new_state=exist_state,
            )

        await action()

    @staticmethod
    async def perform_sending_code(
        message: types.Message, state: FSMContext, email: str, new_state: State
    ):
        data = await HttpChatBot.code_to_email(EmailDto(email=email))

        await state.update_data(EmailCode=data.get("Code"))
        await state.update_data(UserId=data.get("UserId"))

        await message.answer(text=texts.ASKING_CODE, reply_markup=other_email_kb)

        return await state.set_state(new_state)

    @staticmethod
    async def check_code(
        message: types.Message,
        state: FSMContext,
        failure_state: State,
        other_email_action: Callable,
    ):
        data = await state.get_data()

        correct_code = data.get("EmailCode")
        user_text = message.text

        if user_text == texts.OTHER_MAIL:
            return await other_email_action()

        email = data.get("Email")

        if correct_code != user_text:
            await message.answer(texts.WRONG_CODE)
            await EmailHandlers.perform_sending_code(
                message=message, state=state, email=email, new_state=failure_state
            )
            return

        await message.answer(texts.SUCCESSFUL_AUTH)
        await update_user_state_data(state)
        await full_cabinet_menu(message=message, state=state)
