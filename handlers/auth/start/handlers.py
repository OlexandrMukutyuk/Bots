from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import as_marked_section
from aiogram.utils.markdown import hlink

from data.config import WEBSITE_URL
from handlers.auth.common import perform_sending_email_code
from keyboards.default.auth.register import phone_share_kb
from keyboards.default.auth.start import hello_kb, auth_types_kb
from keyboards.default.auth.start import is_register_on_site, start_again_kb, yes_text, no_text
from keyboards.default.basic import yes_n_no
from services.http_client import check_email
from states.auth import StartState, AuthState, AdvancedRegisterState


async def start(message: types.Message, state: FSMContext):
    await message.answer(
        text="😊Вас вітає Контакт Центр!🤝\n\n"
             "Для продовження, натисніть кнопку внизу ⬇️",
        reply_markup=hello_kb
    )

    await state.set_state(StartState.waiting_greeting)


async def greeting(message: types.Message, state: FSMContext):
    await message.answer(
        text=as_marked_section(
            "Зі мною можна швидко та зручно 👇\n",

            "дізнатися про ремонтні роботи міста;",
            "відслідкувати статус актуальних звернень;",
            "переглянути історію звернень;",
            "оцінити роботу підприємств міста;",
            "користуватися довідковою інформацією.",

            marker="✅ ",
        ).as_html()
    )

    await message.answer("Оберіть тип реєстрації, розширена або підписка?", reply_markup=auth_types_kb)
    await message.answer("Розширена реєстрація дозволяє робити звернення та відслідковувати їх статус.")
    await message.answer(
        "Підписка дає можливість оцінити роботу комунальних підприємств, користуватись довідковою інформацією і "
        "отримувати інформацію про проведення ремонтних робіт")

    await state.set_state(StartState.waiting_auth_type)


async def check_user_email(message: types.Message, state: FSMContext):
    email = message.text

    await state.update_data(Email=email)

    temp_message = await message.answer("Зачекайте, будь-ласка, отримую дані")

    is_user_exist = await check_email(email)

    await temp_message.delete()

    if is_user_exist:
        await perform_sending_email_code(message, state, email)

    await asking_if_register(message, state)


async def answer_if_register(message: types.Message, state: FSMContext):
    message_text = message.text

    if message_text == yes_text:
        await asking_if_email_confirmed(message, state)

    if message_text == no_text:
        await message.answer('Потрібно зареєструватись')
        await message.answer('Поділіться вашим номером телефону', reply_markup=phone_share_kb)
        await message.answer('Або впишіть його вручну у форматі 380123456789')
        await state.set_state(AdvancedRegisterState.waiting_phone)


async def answer_if_confirmed_email(message: types.Message, state: FSMContext):
    message_text = message.text

    if message_text == yes_text:
        await message.answer(
            text="Зверніться до служби підтримки",
            reply_markup=start_again_kb
        )

    if message_text == no_text:
        link = hlink('Посилання на наш сайт', WEBSITE_URL)

        await message.answer(
            text=f"Щоб продовжити користуватися чат-ботом, вам потрібно підтвердити ваш e-mail\n\n{link}",
            reply_markup=start_again_kb
        )


async def start_again(message: types.Message, state: FSMContext):
    await state.update_data(Email=None)

    await asking_email(message, state)


async def asking_email(message: types.Message, state: FSMContext):
    await message.answer("Пропишіть свій e-mail 📧")
    await state.set_state(AuthState.waiting_email)


async def asking_if_register(message: types.Message, state: FSMContext):
    await message.answer('Ви реєструвалися на сайті?', reply_markup=is_register_on_site)
    await state.set_state(AuthState.answering_if_register)


async def asking_if_email_confirmed(message: types.Message, state: FSMContext):
    await state.set_state(AuthState.answering_if_confirmed_email)
    await message.answer("Ви підтверджували свій e-mail?", reply_markup=yes_n_no)


'''For other time'''


async def subscription_auth(message: types.Message):
    await message.answer("Subscription")
