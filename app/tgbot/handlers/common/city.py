from typing import Callable

import texts
from aiogram import Bot, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import ReplyKeyboardRemove
from handlers.common.helpers import send_loading_message
from handlers.common.inline_mode import InlineHandlers
from keyboards.default.auth.register import other_location_kb
from keyboards.inline.callbacks import StreetCallbackFactory
from keyboards.inline.streets import choose_street_kb, confirm_street_kb
from services.http_client import HttpChatBot, HttpInfoClient
from states.advanced import AdvancedRegisterStates
from utils.template_engine import render_template


class CityHandlers:
    ListCallback = "StreetsMessageId"
    ConfirmCallback = "StreetMessageId"

    @staticmethod
    async def choose_city(message: types.Message, state: FSMContext, new_state: State, bot: Bot):
        if message.text == 'Мого населений пункту немає в списку':
            await message.answer(text='Введіть ваш населений пункт', reply_markup=ReplyKeyboardRemove())
            await state.set_state(AdvancedRegisterStates.waiting_other_location)
        else:
            await CityHandlers.delete_message(
                chat_id=message.from_user.id, state=state, bot=bot, key=CityHandlers.ListCallback
            )
            data = await CityHandlers.delete_message(
                chat_id=message.from_user.id, state=state, bot=bot, key=CityHandlers.ConfirmCallback
            )

            loading = await send_loading_message(message=message)

            data_streets_data = await HttpChatBot.get_all_city(data={"likefilter": message.text})
            await loading.delete()

            if len(data_streets_data) == 0:
                await message.answer(texts.NOT_FOUND, reply_markup=other_location_kb)
                await message.answer(texts.ASKING_STREET)
                return
            msg = await message.answer(text=texts.PICK_STREET, reply_markup=choose_street_kb)

            await state.set_data(
                {
                    **data,
                    "Streets": data_streets_data,
                    "City": data_streets_data,
                    CityHandlers.ListCallback: msg.message_id,
                }
            )
            await state.set_state(new_state)

    @staticmethod
    async def inline_list(callback: types.InlineQuery, streets_data: list):
        await InlineHandlers.generate_inline_list(
            callback=callback,
            data=streets_data,
            render_func=CityHandlers._inline_markup,
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
    async def message_via_bot(message: types.Message, state: FSMContext, bot: Bot):
        data = await CityHandlers.delete_message(
            chat_id=message.from_user.id, state=state, bot=bot, key=CityHandlers.ListCallback
        )

        await state.update_data({CityHandlers.ConfirmCallback: message.message_id, **data})

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

        #street = await HttpInfoClient.get_street_by_id(street_id)
        city = await HttpInfoClient.get_city_by_id(city_id)
        print(city)
        data = await CityHandlers.delete_message(
            chat_id=callback.from_user.id, state=state, bot=bot, key=CityHandlers.ConfirmCallback
        )
        # print(city_id)
        await state.set_data(
            {
                **data,
                "City": city.get("name"),
                "CityId": city_id,
                "Is_City": True,
                "Streets": None,
            }
        )

        await action()

        return await callback.answer()
