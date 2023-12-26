from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from services.http_client import send_code_to_email
from states.auth import LoginState


async def perform_sending_email_code(message: Message, state: FSMContext, email: str):
    data = await send_code_to_email(email)

    await state.update_data(EmailCode=data.get("Code"))
    await message.answer("Ми відправили вам код на пошту. Впишіть його будь ласка ⬇️")

    return await state.set_state(LoginState.waiting_code)
