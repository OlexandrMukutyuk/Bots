from aiogram import types

from keyboards.default.auth.register import choose_gender_kb


async def not_valid_email(message: types.Message):
    await message.answer("Це не схоже на електронну пошту")
    await message.answer("Впишіть, будь-ласка, валідний email")


async def not_valid_phone(message: types.Message):
    await message.answer("Номер введено невірно, спробуйте ще раз")


async def not_valid_street_name(message: types.Message):
    await message.answer("Для пошуку потрібно мінімум 3 літери")
    await message.answer("Спробуйте ще раз")


async def not_selected_street(message: types.Message):
    await message.answer("Підтвердіть вибрану вулицю")


async def not_valid_flat(message: types.Message):
    await message.answer("Це не схоже на номер, у номері квартири можуть бути тільки цифри.")
    await message.answer("Впишіть номер квартири.")


async def not_valid_gender(message: types.Message):
    await message.answer("Ви ввели недопустиме значення")
    return await message.answer("Вкажіть вашу стать", reply_markup=choose_gender_kb)


async def weak_password(message: types.Message):
    await message.answer("Ви не дотрималися вимог до паролю")
    await message.answer("Будь ласка придумайте пароль 🔐")
    return await message.answer(
        "Вимоги до паролю:\n- латиниця\n- не менше 6 символів довжиною\n- хоча б одна велика буква\n- хоча б одна "
        "маленька буква\n- хоча б одна цифра\n- хоча б один не алфавітно-буквений символ (~! @ # $% ...)")


async def not_valid_first_name(message: types.Message):
    await message.answer("Некоректний формат. Можуть бути тільки букви, апострофи та тире.")
    await message.answer("Впишіть будь-ласка ваше ім'я")


async def not_valid_last_name(message: types.Message):
    await message.answer("Некоректний формат. Можуть бути тільки букви, апострофи та тире.")
    await message.answer("Впишіть будь-ласка ваше прізвище")


async def not_valid_middle_name(message: types.Message):
    await message.answer("Некоректний формат. Можуть бути тільки букви, апострофи та тире.")
    await message.answer("Впишіть будь-ласка ваше по батькові")


async def not_valid_text(message: types.Message):
    await message.answer("Ви ввели невалідний текст")


async def not_valid_comment(message: types.Message):
    await message.answer("Ви ввели невалідний коментар")
    await message.answer("Напишіть, будь-ласка, мінімум 10 символів")
