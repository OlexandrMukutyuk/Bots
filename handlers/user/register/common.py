from aiogram import types

from keyboards.inline.streets import confirm_street_kb

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
        results.append(buidl_inline_street_item(item))

    return results


def buidl_inline_street_item(item: dict) -> types.InlineQueryResultArticle:
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
