import os
from typing import Optional, Callable, NamedTuple

from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import ReplyKeyboardRemove

import texts
from constants import MAX_INLINE_RESULT
from keyboards.inline.callbacks import StreetCallbackFactory
from keyboards.inline.streets import confirm_street_kb, choose_street_kb
from services import http_client
from services.http_client import get_user_params, fetch_streets
from states.auth import LoginState
from utils.template_engine import render_template


class Handler(NamedTuple):
    handler: Callable
    filters: list


class StreetsHandlers:
    @staticmethod
    async def choose_street(message: types.Message, state: FSMContext, new_state: State):
        streets_data = await fetch_streets(message.text)

        if len(streets_data) == 0:
            await message.answer(texts.NOT_FOUND)
            await message.answer(texts.ASKING_STREET)
            return

        await message.answer(text=texts.PICK_STREET, reply_markup=choose_street_kb)

        await state.update_data(Streets=streets_data)
        await state.set_state(new_state)

    @staticmethod
    async def inline_list(callback: types.InlineQuery, streets_data: list):
        await InlineHandlers.generate_inline_list(
            callback=callback,
            data=streets_data,
            render_func=StreetsHandlers.inline_markup,
        )

    @staticmethod
    def inline_markup(street: dict):
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
    async def confirm_street(
        callback: types.CallbackQuery,
        callback_data: StreetCallbackFactory,
        state: FSMContext,
        action: Callable,
    ):
        await state.update_data(
            Streets=None,
            StreetId=callback_data.street_id,
            CityId=callback_data.city_id,
        )

        await action()

        return await callback.answer()


class InlineHandlers:
    @staticmethod
    async def generate_inline_list(callback: types.InlineQuery, data: list, render_func: Callable):
        offset = int(callback.offset or "0")

        results = InlineHandlers.markup_inline_list(data, offset, render_func)

        if len(data) > offset + MAX_INLINE_RESULT:
            next_offset = str(offset + MAX_INLINE_RESULT)
        else:
            next_offset = None

        await callback.answer(results=results, next_offset=next_offset, cache_time=2)

    @staticmethod
    def markup_inline_list(data: list, offset: Optional[int], render_func: Callable):
        results = []

        if offset != None:
            for item in data[offset : offset + MAX_INLINE_RESULT - 1]:
                results.append(render_func(item))

        else:
            for item in data:
                results.append(render_func(item))

        return results


async def perform_sending_email_code(message: types.Message, state: FSMContext, email: str):
    data = await http_client.send_code_to_email(email)

    await state.update_data(EmailCode=data.get("Code"))
    await state.update_data(UserId=data.get("UserId"))

    await message.answer("Ми відправили вам код на пошту. Впишіть його будь ласка ⬇️")

    return await state.set_state(LoginState.waiting_code)


async def generate_inline_street_list(state_data: dict, callback: types.InlineQuery):
    streets_data = state_data["Streets"]
    offset = int(callback.offset or "0")

    results = build_inline_street_list(streets_data, offset)

    if len(streets_data) > offset + MAX_INLINE_RESULT:
        next_offset = str(offset + MAX_INLINE_RESULT)
    else:
        next_offset = None

    await callback.answer(results=results, next_offset=next_offset, cache_time=2)


def build_inline_street_list(streets: list, offset: int) -> list[types.InlineQueryResultArticle]:
    results = []

    for item in streets[offset : offset + MAX_INLINE_RESULT - 1]:
        results.append(build_inline_street_item(item))

    return results


def build_inline_street_item(item: dict) -> types.InlineQueryResultArticle:
    id = item["Id"]
    title = item["Type"] + " " + item["Name"]

    return types.InlineQueryResultArticle(
        id=str(id),
        title=title,
        description=item["City"],
        input_message_content=types.InputTextMessageContent(
            message_text=f"<b>{title}</b>\n{item['City']}\n\nПідтверджуйте 👇"
        ),
        reply_markup=confirm_street_kb(street_id=id, city_id=item["CityId"]),
    )


async def update_user_state_data(state: FSMContext):
    data = await state.get_data()

    user_id = data.get("UserId")

    user_params = await get_user_params(user_id)

    await state.set_data({"UserId": user_id, **user_params})


def delete_tmp_media(media_ids):
    if not media_ids or not len(media_ids):
        return

    for media_id in media_ids:
        file_path = f"{os.getcwd()}/tmp/{media_id}"

        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except OSError as e:
                print(f"Error deleting file {file_path}: {e}")
        else:
            print(f"File not found: {file_path}")


async def send_loading_message(message: types.Message):
    return await message.answer(text=texts.LOADING, reply_markup=ReplyKeyboardRemove())


async def independent_message(text: str, reply_markup, **kwargs):
    message: types.Message = kwargs.get("message")

    if message:
        await message.answer(text=text, reply_markup=reply_markup)
    else:
        bot: Bot = kwargs.get("bot")
        chat_id: int = kwargs.get("chat_id")

        await bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
