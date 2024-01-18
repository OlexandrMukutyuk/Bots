from aiogram import types
from aiogram.fsm.context import FSMContext

from dto.chat_bot import ReportIssueDto
from handlers.common.helpers import full_cabinet_menu
from services.http_client import HttpChatBot


async def report_tech_issue(message: types.Message, state: FSMContext):
    user_data = await state.get_data()

    await HttpChatBot.report_issue(
        ReportIssueDto(user_id=user_data.get("UserId"), comment=message.text)
    )

    await message.answer("Звернення відправлено успішно!")

    return await full_cabinet_menu(state, message=message)
