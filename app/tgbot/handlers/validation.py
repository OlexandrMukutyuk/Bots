from aiogram import types

import texts
from keyboards.default.auth.register import choose_gender_kb
from keyboards.default.common import back_kb


async def not_valid_email(message: types.Message):
    await message.answer(texts.NOT_VALID_EMAIL)
    await message.answer(texts.ASKING_EMAIL)


async def not_valid_phone(message: types.Message):
    await message.answer(texts.NOT_VALID_PHONE)


async def not_valid_street_name(message: types.Message):
    await message.answer(texts.NOT_VALID_STREET_NAME)
    await message.answer(texts.TRY_AGAIN)


async def not_valid_flat(message: types.Message):
    await message.answer(texts.NOT_VALID_FLAT)
    await message.answer(texts.ASKING_FLAT)


async def not_valid_gender(message: types.Message):
    await message.answer("Ви ввели недопустиме значення")
    return await message.answer("Вкажіть вашу стать", reply_markup=choose_gender_kb)


async def weak_password(message: types.Message):
    await message.answer(texts.WEAK_PASSWORD)
    await message.answer(texts.ASKING_PASSWORD)
    return await message.answer(texts.PASSWORD_REQS)


async def not_valid_first_name(message: types.Message):
    await message.answer(texts.NOT_VALID_NAME)
    await message.answer(texts.ASKING_FIRST_NAME)


async def not_valid_last_name(message: types.Message):
    await message.answer(texts.NOT_VALID_NAME)
    await message.answer(texts.ASKING_LAST_NAME)


async def not_valid_middle_name(message: types.Message):
    await message.answer(texts.NOT_VALID_NAME)
    await message.answer(texts.ASKING_MIDDLE_NAME)


async def not_valid_text(message: types.Message):
    await message.answer(texts.NOT_VALID_TEXT)


async def not_valid_text_with_back(message: types.Message):
    await message.answer(text=texts.NOT_VALID_TEXT, reply_markup=back_kb)


async def not_valid_comment(message: types.Message):
    await message.answer(texts.NOT_VALID_COMMENT)
    await message.answer(texts.ASKING_MIN_10_CHARS)
