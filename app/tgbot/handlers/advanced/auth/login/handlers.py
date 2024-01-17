from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from handlers.advanced.cabinet.menu.handlers import give_cabinet_menu
from handlers.common.helpers import update_user_state_data, perform_sending_email_code


async def check_email_code(message: Message, state: FSMContext):
    data = await state.get_data()

    correct_code = data.get("EmailCode")
    user_code = message.text

    email = data.get("Email")

    if correct_code != user_code:
        await message.answer("Код невірний. Спробуйте ще раз")
        return await perform_sending_email_code(message, state, email)

    await message.answer("Вітаю, ви успішно увійшли у свій аккаунт")

    await update_user_state_data(state)

    return await give_cabinet_menu(message=message, state=state)
