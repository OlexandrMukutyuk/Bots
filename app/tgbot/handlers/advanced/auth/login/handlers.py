from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from handlers.common.email import EmailHandlers
from handlers.start.handlers import asking_email
from states import LoginState


async def check_email_code(message: Message, state: FSMContext):
    async def action():
        return await asking_email(message, state)

    await EmailHandlers.check_code(
        message=message,
        state=state,
        failure_state=LoginState.waiting_code,
        other_email_action=action,
    )
