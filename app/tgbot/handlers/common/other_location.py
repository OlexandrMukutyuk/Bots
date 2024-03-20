from typing import Callable

from aiogram import Bot, types
from aiogram.fsm.context import FSMContext
from handlers.common.helpers import send_loading_message
from keyboards.inline.callbacks import StreetCallbackFactory
from keyboards.inline.streets import confirm_street_kb
from utils.template_engine import render_template


class OtherLocationHandlers:
    ListCallback = "StreetsMessageId"
    ConfirmCallback = "StreetMessageId"

    @staticmethod
    async def take_other_location(message: types.Message, state: FSMContext, bot: Bot,
                                  data_streets_data: str):
        await OtherLocationHandlers.delete_message(
            chat_id=message.from_user.id, state=state, bot=bot, key=OtherLocationHandlers.ListCallback
        )
        data = await OtherLocationHandlers.delete_message(
            chat_id=message.from_user.id, state=state, bot=bot, key=OtherLocationHandlers.ConfirmCallback
        )

        loading = await send_loading_message(message=message)

        data_streets_data = data_streets_data
        await loading.delete()

        street = {'id': 1, 'name': data_streets_data}
        inline_query_result = OtherLocationHandlers._inline_markup(street)

        msg = await bot.send_message(
            chat_id=message.chat.id,
            text=inline_query_result.input_message_content.message_text,
            reply_markup=inline_query_result.reply_markup
        )

        await state.set_data(
            {
                **data,
                "Streets": data_streets_data,
                "City": data_streets_data,
                OtherLocationHandlers.ListCallback: msg.message_id,
            }
        )

    @staticmethod
    def _inline_markup(street: dict):
        id = street["id"]
        title = street["name"]

        return types.InlineQueryResultArticle(
            id=str(id),
            title=title,
            input_message_content=types.InputTextMessageContent(
                message_text=render_template("confirm_street.j2", title=title)
            ),
            reply_markup=confirm_street_kb(street_id=id, city_id=street["id"]),
        )

    @staticmethod
    async def delete_message(chat_id: int, state: FSMContext, bot: Bot, key: str) -> dict:
        data = await state.get_data()
        msg_id = data.get(key)

        if msg_id:
            await bot.delete_message(chat_id, msg_id)
            del data[key]
            await state.set_data(data)

        return data

    @staticmethod
    async def confirm_other_location(
            callback: types.CallbackQuery,
            callback_data: StreetCallbackFactory,
            state: FSMContext,
            action: Callable,
            bot: Bot,
    ):
        info_user = await state.get_data()
        city = info_user['City']
        print(city)
        data = await OtherLocationHandlers.delete_message(
            chat_id=callback.from_user.id, state=state, bot=bot, key=OtherLocationHandlers.ConfirmCallback
        )
        # print(city_id)
        await state.set_data(
            {
                **data,
                "City": city,
                "Streets": None,
            }
        )

        await action()

        return await callback.answer()
