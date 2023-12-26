from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from handlers.common import generate_inline_street_list
from keyboards.default.auth.edit_info import edit_text, edit_register_info_kb
from keyboards.default.auth.register import without_flat_kb, phone_share_kb, without_flat_text
from keyboards.inline.callbacks import StreetCallbackFactory
from keyboards.inline.streets import choose_street_kb
from services.http_client import fetch_streets, verify_address
from states.auth import EditRegisterState


async def fill_data(message: types.Message, state: FSMContext):
    await state.update_data(
        Email="siifsfj@gmail.com",
        FirstName="Dima",
        MiddleName="Kacev",
        LastName="Bot",
        Phone="+380874084248",
        Password="SHIT",
        StreetId="2424",
        House="fsjief",
    )

    await state.set_state(EditRegisterState.waiting_accepting)

    await message.answer("Done")


async def handle_buttons(message: types.Message, state: FSMContext):
    button_type = message.text

    if button_type == edit_text['first_name_text']:
        await state.set_state(EditRegisterState.waiting_first_name)
        return await message.answer("Впишіть будь-ласка ваше ім'я", reply_markup=ReplyKeyboardRemove())

    if button_type == edit_text['middle_name_text']:
        await state.set_state(EditRegisterState.waiting_middle_name)
        return await message.answer("Впишіть будь-ласка ваше прізвище", reply_markup=ReplyKeyboardRemove())

    if button_type == edit_text['last_name_text']:
        await state.set_state(EditRegisterState.waiting_last_name)
        return await message.answer("Впишіть будь-ласка ваше по батькові", reply_markup=ReplyKeyboardRemove())

    if button_type == edit_text['phone_text']:
        await state.set_state(EditRegisterState.waiting_phone)
        await message.answer('Поділіться вашим номером телефону', reply_markup=phone_share_kb)
        return await message.answer('Або впишіть його вручну у форматі 380123456789')

    if button_type == edit_text['password_text']:
        await state.set_state(EditRegisterState.waiting_password)
        await message.answer("Будь ласка придумайте пароль 🔐", reply_markup=ReplyKeyboardRemove())
        return await message.answer(
            "Вимоги до паролю:\n"
            "- латиниця\n"
            "- не менше 6 символів довжиною\n"
            "- хоча б одна велика буква\n"
            "- хоча б одна маленька буква\n"
            "- хоча б одна цифра\n"
            "- хоча б один не алфавітно-буквений символ (~! @ # $% ...)"
        )

    if button_type == edit_text['street_text']:
        await state.set_state(EditRegisterState.waiting_street_typing)
        return await message.answer('Впишіть назву вашої вулиці (мінімум 3 літери) 🏙️',
                                    reply_markup=ReplyKeyboardRemove())

    if button_type == edit_text['house_text']:
        await state.set_state(EditRegisterState.waiting_house)
        return await message.answer("Впишіть будь ласка номер будинку 🏠", reply_markup=ReplyKeyboardRemove())

    if button_type == edit_text['flat_text']:
        await state.set_state(EditRegisterState.waiting_flat)
        return await message.answer(
            text="Впишіть номер квартири. (Якщо мешкаєте у своєму домі, жміть кнопку знизу)",
            reply_markup=without_flat_kb
        )


async def first_time_showing_user_info(message: types.Message, state: FSMContext):
    await send_user_info(state, message=message)


async def send_user_info(state: FSMContext, **kwargs):
    user_data = await state.get_data()

    for key, value in user_data.items():
        print(f"{key}: {value}")

    info_text = (
        f"Пошта: {user_data.get('Email')}\n\n"
        f"Ім'я: {user_data.get('FirstName')}\n"
        f"Прізвище: {user_data.get('MiddleName')}\n"
        f"По батькові: {user_data.get('LastName')}\n"
        f"Телефон: {user_data.get('Phone')}\n"
        f"Пароль: {user_data.get('Password')}\n"
        f"Вулиця: {user_data.get('StreetId')}\n"
        f"Номер будинку: {user_data.get('House')}\n\n"
        "Підтверджуйте 👇"
    )

    asking_text = 'Все вірно, чи необхідно щось змінити?'

    message: types.Message = kwargs.get('message')

    if message:
        await send_info_by_message(info_text, asking_text, message)
    else:
        await send_info_by_bot(info_text, asking_text, **kwargs)


async def send_info_by_message(info_text: str, asking_text: str, message: types.Message):
    await message.answer(text=info_text)
    await message.answer(
        text=asking_text,
        reply_markup=edit_register_info_kb
    )


async def send_info_by_bot(info_text: str, asking_text: str, **kwargs):
    bot: Bot = kwargs.get('bot')
    chat_id = kwargs.get('chat_id')

    await bot.send_message(chat_id=chat_id, text=info_text)
    await bot.send_message(chat_id=chat_id, text=asking_text, reply_markup=edit_register_info_kb)


async def edit_phone(message: types.Message, state: FSMContext):
    phone = message.text or message.contact.phone_number

    await state.update_data(Phone=phone)
    await state.set_state(EditRegisterState.waiting_accepting)

    await send_user_info(state, message=message)


async def edit_street(message: types.Message, state: FSMContext):
    streets_data = await fetch_streets(message.text)

    if len(streets_data) == 0:
        await message.answer("Пошук не дав результатів")
        return await message.answer("Впишіть назву вашої вулиці (мінімум 3 літери) 🏙️")

    await message.answer('Виберіть вулицю з кнопок нижче! 👇', reply_markup=choose_street_kb)

    await state.update_data(Streets=streets_data)

    await state.set_state(EditRegisterState.waiting_street_selected)


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

    await state.set_state(EditRegisterState.waiting_accepting)

    await send_user_info(state, bot=bot, chat_id=callback.from_user.id)

    return await callback.answer()


async def edit_house(message: types.Message, state: FSMContext):
    house = message.text

    street_id = (await state.get_data())["StreetId"]

    is_address_correct = await verify_address(street_id=street_id, house=house)

    if not is_address_correct:
        await message.answer("Такого будинку не знайдено")
        return await message.answer(
            text="Впишіть будь ласка номер будинку 🏠",
        )

    await state.update_data(House=house)

    await state.set_state(EditRegisterState.waiting_accepting)

    await send_user_info(state, message=message)


async def edit_flat(message: types.Message, state: FSMContext):
    flat = message.text

    if flat == without_flat_text:
        flat = None

    await state.update_data(Flat=flat)
    await state.set_state(EditRegisterState.waiting_accepting)

    await send_user_info(state, message=message)


async def edit_first_name(message: types.Message, state: FSMContext):
    first_name = message.text

    await state.update_data(FirstName=first_name)
    await state.set_state(EditRegisterState.waiting_accepting)

    await send_user_info(state, message=message)


async def edit_middle_name(message: types.Message, state: FSMContext):
    middle_name = message.text

    await state.update_data(MiddleName=middle_name)
    await state.set_state(EditRegisterState.waiting_accepting)

    await send_user_info(state, message=message)


async def edit_last_name(message: types.Message, state: FSMContext):
    last_name = message.text

    await state.update_data(LastName=last_name)
    await state.set_state(EditRegisterState.waiting_accepting)

    await send_user_info(state, message=message)


async def edit_password(message: types.Message, state: FSMContext):
    await state.update_data(Password=message.text)
    await state.set_state(EditRegisterState.waiting_accepting)

    await send_user_info(state, message=message)


async def accept_info(message: types.Message, state: FSMContext):
    data = await state.get_data()

    # TODO Register auth
    for key, value in data.items():
        print(f"{key}: {value}")
