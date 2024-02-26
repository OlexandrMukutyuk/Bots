from typing import Callable

from aiogram import Bot, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

import texts
from dto.chat_bot import SearchDto
from handlers.common.helpers import send_loading_message
from handlers.common.inline_mode import InlineHandlers
from keyboards.inline.callbacks import StreetCallbackFactory
from keyboards.inline.streets import choose_street_kb, confirm_street_kb
from services.http_client import HttpChatBot, HttpInfoClient
from utils.template_engine import render_template


class StreetsHandlers:
    ListCallback = "StreetsMessageId"
    ConfirmCallback = "StreetMessageId"

    @staticmethod
    async def choose_street(message: types.Message, state: FSMContext, new_state: State, bot: Bot):
        await StreetsHandlers.delete_message(
            chat_id=message.from_user.id, state=state, bot=bot, key=StreetsHandlers.ListCallback
        )

        data = await StreetsHandlers.delete_message(
            chat_id=message.from_user.id, state=state, bot=bot, key=StreetsHandlers.ConfirmCallback
        )

        loading = await send_loading_message(message=message)

        streets_data = await HttpChatBot.fetch_streets(SearchDto(search=message.text))

        await loading.delete()

        if len(streets_data) == 0:
            await message.answer(texts.NOT_FOUND)
            await message.answer(texts.ASKING_STREET)
            return

        msg = await message.answer(text=texts.PICK_STREET, reply_markup=choose_street_kb)

        await state.set_data(
            {
                **data,
                "Streets": streets_data,
                StreetsHandlers.ListCallback: msg.message_id,
            }
        )
        await state.set_state(new_state)

    @staticmethod
    async def inline_list(callback: types.InlineQuery, streets_data: list):
        await InlineHandlers.generate_inline_list(
            callback=callback,
            data=streets_data,
            render_func=StreetsHandlers._inline_markup,
        )

    @staticmethod
    def _inline_markup(street: dict):
        id = street["Id"]
        title = street["Type"] + " " + street["Name"]
        city = street["City"]

        return types.InlineQueryResultArticle(
            id=str(id),
            title=title,
            description=city,
            input_message_content=types.InputTextMessageContent(
                message_text=render_template("confirm_street.j2", title=title, city=city)
            ),
            reply_markup=confirm_street_kb(street_id=id, city_id=street["CityId"]),
        )

    @staticmethod
    async def message_via_bot(message: types.Message, state: FSMContext, bot: Bot):
        data = await StreetsHandlers.delete_message(
            chat_id=message.from_user.id, state=state, bot=bot, key=StreetsHandlers.ListCallback
        )

        await state.update_data({StreetsHandlers.ConfirmCallback: message.message_id, **data})

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
    async def confirm_street(
            callback: types.CallbackQuery,
            callback_data: StreetCallbackFactory,
            state: FSMContext,
            action: Callable,
            bot: Bot,
    ):
        street_id = callback_data.street_id
        city_id = callback_data.city_id

        street = await HttpInfoClient.get_street_by_id(street_id)
        city = await HttpInfoClient.get_city_by_id(city_id)

        data = await StreetsHandlers.delete_message(
            chat_id=callback.from_user.id, state=state, bot=bot, key=StreetsHandlers.ConfirmCallback
        )

        await state.set_data(
            {
                **data,
                "Street": street.get("name"),
                "City": city.get("name"),
                "StreetId": street_id,
                "CityId": city_id,
                "Streets": None,
            }
        )

        await action()

        return await callback.answer()
