from typing import Optional

from aiogram import Bot, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

import texts
from dto.chat_bot import ParentIdDto
from handlers.common.helpers import send_loading_message, independent_message
from keyboards.inline.cabinet.reference_info import generate_ref_info_kb
from keyboards.inline.callbacks import ReferenceInfoCallbackFactory
from services.http_client import HttpChatBot
from utils.template_engine import render_template


class ReferenceInfoHandlers:

    @staticmethod
    async def load_menu(state: FSMContext, parent_id: Optional[int], new_state: Optional[State], **kwargs):
        loading = await send_loading_message(**kwargs)

        ref_info = await HttpChatBot.get_information(ParentIdDto(parent_id=parent_id))

        await loading.delete()

        await state.update_data(ReferenceInfo=ref_info)

        if new_state:
            await state.set_state(new_state)

        await independent_message(
            text=texts.ASKING_REF_INFO,
            reply_markup=generate_ref_info_kb(ref_info),
            **kwargs
        )

    @staticmethod
    async def show_info(
            callback: types.CallbackQuery,
            callback_data: ReferenceInfoCallbackFactory,
            state: FSMContext,
            bot: Bot
    ):
        chat_id = callback.from_user.id
        data = await state.get_data()
        ref_info = data.get('ReferenceInfo')
        current_info_id = callback_data.id

        target_info = next((info for info in ref_info if info.get('Id') == current_info_id), None)

        if target_info.get("Description") is None:
            await callback.message.delete()

            await ReferenceInfoHandlers.load_menu(
                state=state,
                parent_id=current_info_id,
                bot=bot,
                chat_id=chat_id,
                new_state=None
            )

        else:
            await callback.message.delete()

            await bot.send_message(
                text=render_template('show_ref_info.j2', info=target_info),
                chat_id=chat_id
            )

            await bot.send_message(
                text=texts.ASKING_REF_INFO,
                reply_markup=generate_ref_info_kb(ref_info),
                chat_id=chat_id
            )

        await callback.answer()
