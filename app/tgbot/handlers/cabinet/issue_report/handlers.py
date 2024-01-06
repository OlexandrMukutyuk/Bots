from aiogram import types
from aiogram.fsm.context import FSMContext

from app.tgbot.handlers.cabinet.menu.handlers import give_cabinet_menu
from app.tgbot.services import http_client


async def report_tech_issue(message: types.Message, state: FSMContext):
    user_data = await state.get_data()

    await http_client.report_issue({
        "UserId": user_data.get('UserId'),
        "Comment": message.text
    })

    await message.answer('Звернення відправлено успішно!')

    return await give_cabinet_menu(state, message=message)
