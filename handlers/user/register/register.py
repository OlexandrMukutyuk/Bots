from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from handlers.user.register.common import generate_inline_street_list
from keyboards.default.user.register import (
    phone_share_kb,
    change_street_kb,
    without_flat_kb,
    without_flat_text,
    choose_gender_kb, gender_dict, registration_agreement_kb
)
from keyboards.inline.callbacks import StreetCallbackFactory
from keyboards.inline.streets import choose_street_kb
from services.http_client import fetch_streets, verify_address
from states.user import AdvancedRegisterState

MAX_INLINE_RESULT = 50


async def start(message: types.Message, state: FSMContext):
    await message.answer('Потрібно зареєструватись')

    await message.answer('Поділіться вашим номером телефону', reply_markup=phone_share_kb)
    await message.answer('Або впишіть його вручну у форматі 380123456789')

    await state.set_state(AdvancedRegisterState.waiting_phone)


async def save_phone(message: types.Message, state: FSMContext):
    phone = message.text or message.contact.phone_number

    await state.update_data(Phone=phone)
    await message.answer("Ваш номер успішно відправлено")

    await state.set_state(AdvancedRegisterState.waiting_street_typing)
    await message.answer('Впишіть назву вашої вулиці (мінімум 3 літери) 🏙️', reply_markup=ReplyKeyboardRemove())


async def choose_street(message: types.Message, state: FSMContext):
    streets_data = await fetch_streets(message.text)

    if len(streets_data) == 0:
        await message.answer("Пошук не дав результатів")
        return await message.answer("Впишіть назву вашої вулиці (мінімум 3 літери) 🏙️")

    await message.answer('Виберіть вулицю з кнопок нижче! 👇', reply_markup=choose_street_kb)

    await state.update_data(Streets=streets_data)

    await state.set_state(AdvancedRegisterState.waiting_street_selected)


async def show_street_list(callback: types.InlineQuery, state: FSMContext):
    data = await state.get_data()

    await generate_inline_street_list(data, callback)


async def confirm_street(
        callback: types.CallbackQuery,
        callback_data: StreetCallbackFactory,
        state: FSMContext,
        bot: Bot
):
    await state.update_data(
        Streets=None,
        StreetId=callback_data.street_id,
        CityId=callback_data.city_id,
    )

    await bot.send_message(
        chat_id=callback.from_user.id,
        text="Впишіть будь ласка номер будинку 🏠",
        reply_markup=change_street_kb
    )

    await state.set_state(AdvancedRegisterState.waiting_house)

    return await callback.answer()


async def change_street(message: types.Message, state: FSMContext):
    await state.set_state(AdvancedRegisterState.waiting_street_typing)
    await message.answer('Впишіть назву вашої вулиці (мінімум 3 літери) 🏙️', reply_markup=ReplyKeyboardRemove())


async def save_house(message: types.Message, state: FSMContext):
    house = message.text

    street_id = (await state.get_data())["StreetId"]

    is_address_correct = await verify_address(street_id=street_id, house=house)

    if not is_address_correct:
        await message.answer("Такого будинку не знайдено")
        return await message.answer(
            text="Впишіть будь ласка номер будинку 🏠",
            reply_markup=change_street_kb
        )

    await state.update_data(House=house)

    await state.set_state(AdvancedRegisterState.waiting_flat)

    await message.answer(
        text="Впишіть номер квартири. (Якщо мешкаєте у своєму домі, жміть кнопку знизу)",
        reply_markup=without_flat_kb
    )


async def save_flat(message: types.Message, state: FSMContext):
    flat = message.text

    if flat == without_flat_text:
        flat = None

    await state.update_data(Flat=flat)
    await state.set_state(AdvancedRegisterState.waiting_first_name)

    return await message.answer("Впишіть будь-ласка ваше ім'я", reply_markup=None)


async def save_first_name(message: types.Message, state: FSMContext):
    first_name = message.text

    await state.update_data(FirstName=first_name)
    await state.set_state(AdvancedRegisterState.waiting_middle_name)

    return await message.answer("Впишіть будь-ласка ваше прізвище")


async def save_middle_name(message: types.Message, state: FSMContext):
    middle_name = message.text

    await state.update_data(MiddleName=middle_name)
    await state.set_state(AdvancedRegisterState.waiting_last_name)

    return await message.answer("Впишіть будь-ласка ваше по батькові")


async def save_last_name(message: types.Message, state: FSMContext):
    last_name = message.text

    await state.update_data(LastName=last_name)
    await state.set_state(AdvancedRegisterState.waiting_gender)

    return await message.answer(
        text="Вкажіть вашу стать",
        reply_markup=choose_gender_kb
    )


async def save_gender(message: types.Message, state: FSMContext):
    gender = message.text

    if gender == gender_dict['other']:
        gender = None

    await state.update_data(Gender=gender)
    await state.set_state(AdvancedRegisterState.waiting_password)

    await message.answer("Будь ласка придумайте пароль 🔐")
    return await message.answer(
        "Вимоги до паролю:\n- латиниця\n- не менше 6 символів довжиною\n- хоча б одна велика буква\n- хоча б одна "
        "маленька буква\n- хоча б одна цифра\n- хоча б один не алфавітно-буквений символ (~! @ # $% ...)")


async def save_password(message: types.Message, state: FSMContext):
    await state.update_data(Password=message.text)
    await state.set_state(AdvancedRegisterState.waiting_agreement)

    return await show_agreement(message)


async def show_agreement(message: types.Message):
    return await message.answer(
        text="Щоб продовжити користуватися чат-ботом ви погоджуєтесь зі збереженням та обробкою "
             "персональних даних згідно Закону України «Про захист персональних даних» та "
             "підтверджуєте, що не розміщуватимите інформацію з обмеженим доступом\n\n<a href= "
             "'https://zakon.rada.gov.ua/laws/show/2297-17#Text'>https://zakon.rada.gov.ua/laws"
             "/show/2297-17#Text</a>",
        reply_markup=registration_agreement_kb
    )
