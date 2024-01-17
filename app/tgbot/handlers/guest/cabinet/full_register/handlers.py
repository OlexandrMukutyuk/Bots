from aiogram.fsm.context import FSMContext
from aiogram.types import Message


async def begin_full_registration(message: Message, state: FSMContext):
    await message.answer("Full started")
    pass
