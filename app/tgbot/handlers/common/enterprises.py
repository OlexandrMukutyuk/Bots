from typing import Callable

from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

import texts
from handlers.common.helpers import send_loading_message, independent_message
from keyboards.inline.cabinet.rate_enterprises import enterprises_list_kb, enterprises_rates_kb
from keyboards.inline.callbacks import EnterpriseCallbackFactory
from utils.template_engine import render_template


class EnterprisesHandlers:
    @staticmethod
    async def enterprises_list(
        state: FSMContext,
        get_enterprises: Callable,
        new_state: State,
        menu_callback: Callable,
        **kwargs,
    ):
        loading_msg = None

        callback: types.CallbackQuery | None = kwargs.get("callback", None)
        bot: Bot | None = kwargs.get("bot", None)

        if not callback:
            loading_msg = await send_loading_message(**kwargs)

        enterprises = await get_enterprises()
        allowed_to_rate = list(filter(lambda item: item.get("CanVote"), enterprises))

        if not callback and loading_msg:
            await loading_msg.delete()

        if len(allowed_to_rate) == 0:
            await independent_message(texts.NO_ENTERPRISES_TO_RATE, **kwargs)
            return await menu_callback()

        if callback:
            await bot.edit_message_text(
                text=texts.ASKGING_ENTERPRISE,
                message_id=callback.message.message_id,
                chat_id=callback.from_user.id,
                reply_markup=enterprises_list_kb(allowed_to_rate),
            )

        else:
            await independent_message(
                text=texts.ASKGING_ENTERPRISE,
                reply_markup=enterprises_list_kb(allowed_to_rate),
                **kwargs,
            )

        await state.set_state(new_state)

    @staticmethod
    async def show_rate_for_enterprises(
        callback: types.CallbackQuery,
        callback_data: EnterpriseCallbackFactory,
        state: FSMContext,
        bot: Bot,
        enterprises: list[dict],
        new_state: State,
    ):
        enterprise_id = callback_data.enterprise_id

        message_id = callback.message.message_id

        enterprise_name = ""
        for enterprise in enterprises:
            if enterprise.get("Id") == enterprise_id:
                enterprise_name = enterprise.get("Name")

        chat_id = callback.from_user.id

        await state.set_state(new_state)

        await bot.edit_message_text(
            text=render_template("rate_enterprise.j2", title=enterprise_name),
            message_id=message_id,
            chat_id=chat_id,
            reply_markup=enterprises_rates_kb(enterprise_id=enterprise_id),
        )

    @staticmethod
    async def rate_enterprise(callback: types.CallbackQuery, rate: int, bot: Bot, action: Callable):
        chat_id = callback.from_user.id

        await bot.send_message(chat_id=chat_id, text=f"Оцінка {rate} ⭐️")
        await bot.send_message(chat_id=chat_id, text="Ваша оцінка відправлена успішно")

        await callback.message.delete()

        return await action()

    # Back handlers
    @staticmethod
    async def to_menu(callback: types.CallbackQuery, state: FSMContext, action: Callable):
        chat_id = callback.from_user.id

        await callback.message.delete()

        return await action()
