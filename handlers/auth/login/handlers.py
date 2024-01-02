from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from handlers.auth.common import perform_sending_email_code


async def check_email_code(message: Message, state: FSMContext):
    data = await state.get_data()

    correct_code = data.get("EmailCode")
    user_code = message.text

    email = data.get("Email")

    if correct_code != user_code:
        await message.answer("Код невірний. Спробуйте ще раз")
        return await perform_sending_email_code(message, state, email)

    await message.answer("Вітаю, ви успішно увійшли у свій аккаунт")
    # End here: Get user info and login user
    full_user_info = None
