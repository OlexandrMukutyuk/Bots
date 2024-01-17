from typing import Callable

from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

import texts
from handlers.common.helpers import send_loading_message
from keyboards.inline.cabinet.rate_enterprises import enterprises_list_kb, enterprises_rates_kb
from keyboards.inline.callbacks import EnterpriseCallbackFactory
from utils.template_engine import render_template


class EnterprisesHandlers:
    @staticmethod
    async def enterprises_list(
        message: types.Message,
        state: FSMContext,
        get_enterprises: Callable,
        new_state: State,
        menu_callback: Callable,
    ):
        loading_msg = await send_loading_message(message)

        enterprises = await get_enterprises()

        allowed_to_rate = list(filter(lambda item: item.get("CanVote"), enterprises))

        await loading_msg.delete()

        if len(allowed_to_rate) == 0:
            await message.answer(texts.NO_ENTERPRISES_TO_RATE)
            return await menu_callback()

        await message.answer(
            text=texts.ASKGING_ENTERPRISE,
            reply_markup=enterprises_list_kb(allowed_to_rate),
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


#
#
# async def rate_enterprise(
#     callback: types.CallbackQuery,
#     callback_data: EnterpriseRateCallbackFactory,
#     state: FSMContext,
#     bot: Bot,
# ):
#     user_id = (await state.get_data()).get("UserId")
#     chat_id = callback.from_user.id
#
#     rate = callback_data.rate
#     enterprise_id = callback_data.enterprise_id
#
#     status = await HttpChatBot.rate_enterprise(
#         RateEnterpriseDto(user_id=user_id, enterprise_id=enterprise_id, rate=rate)
#     )
#
#     await bot.send_message(chat_id=chat_id, text=f"Оцінка {rate} ⭐️")
#     await bot.send_message(chat_id=chat_id, text="Ваша оцінка відправлена успішно")
#
#     await callback.message.delete()
#
#     return await give_cabinet_menu(state, bot=bot, chat_id=chat_id)
#
#
# # Back handlers
#
#
# async def to_menu(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
#     chat_id = callback.from_user.id
#
#     await callback.message.delete()
#
#     return await give_cabinet_menu(state, bot=bot, chat_id=chat_id)
#
#
# async def to_enterprise_list(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
#     user_data = await state.get_data()
#     chat_id = callback.from_user.id
#
#     message_id = callback.message.message_id
#
#     enterprises = await http_client.get_enterprises(user_id=user_data.get("UserId"))
#
#     allowed_to_rate = list(filter(lambda item: item.get("CanVote"), enterprises))
#
#     if len(allowed_to_rate) == 0:
#         await bot.send_message(
#             chat_id=chat_id, text="Наразі для вас немає доступних для оцінювання підприємств"
#         )
#         return await give_cabinet_menu(state, bot=bot, chat_id=chat_id)
#
#     await bot.edit_message_text(
#         text="Оберіть підприємство, яке ви хотіли би оцінити ⭐️",
#         message_id=message_id,
#         chat_id=chat_id,
#         reply_markup=enterprises_list_kb(allowed_to_rate),
#     )
#
#     await state.set_state(RateEnterprise.showing_list)
