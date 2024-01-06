import os

from aiogram import types
from aiogram.fsm.context import FSMContext

from app.tgbot.keyboards.inline.streets import confirm_street_kb
from app.tgbot.services.http_client import get_user_params

MAX_INLINE_RESULT = 50


async def generate_inline_street_list(state_data: dict, callback: types.InlineQuery):
    streets_data = state_data['Streets']
    offset = int(callback.offset or "0")

    results = build_inline_street_list(streets_data, offset)

    if len(streets_data) > offset + MAX_INLINE_RESULT:
        next_offset = str(offset + MAX_INLINE_RESULT)
    else:
        next_offset = None

    await callback.answer(results=results, next_offset=next_offset, cache_time=2)


def build_inline_street_list(streets: list, offset: int) -> list[types.InlineQueryResultArticle]:
    results = []

    for item in streets[offset: offset + MAX_INLINE_RESULT - 1]:
        results.append(build_inline_street_item(item))

    return results


def build_inline_street_item(item: dict) -> types.InlineQueryResultArticle:
    id = item['Id']
    title = item['Type'] + " " + item['Name']

    return types.InlineQueryResultArticle(
        id=str(id),
        title=title,
        description=item['City'],
        input_message_content=types.InputTextMessageContent(
            message_text=f"<b>{title}</b>\n{item['City']}\n\nПідтверджуйте 👇"
        ),
        reply_markup=confirm_street_kb(street_id=id, city_id=item['CityId'])
    )


async def update_user_state_data(state: FSMContext):
    data = await state.get_data()

    user_id = data.get("UserId")

    user_params = await get_user_params(user_id)

    await state.set_data({
        "UserId": user_id,
        **user_params
    })


def delete_tmp_media(media_ids):
    if not media_ids or not len(media_ids):
        return

    for media_id in media_ids:
        file_path = f'{os.getcwd()}/tmp/{media_id}'

        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except OSError as e:
                print(f"Error deleting file {file_path}: {e}")
        else:
            print(f"File not found: {file_path}")
