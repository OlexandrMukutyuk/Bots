from aiogram.utils.formatting import as_marked_section

GREETING = "😊Вас вітає Контакт Центр!🤝\n\nДля продовження, натисніть кнопку внизу ⬇️"

INTRODUCTION = as_marked_section(
    "Зі мною можна швидко та зручно 👇\n",
    "дізнатися про ремонтні роботи міста;",
    "відслідкувати статус актуальних звернень;",
    "переглянути історію звернень;",
    "оцінити роботу підприємств міста;",
    "користуватися довідковою інформацією.",
    marker="✅ ",
).as_html()

PICK_AUTH_TYPE = "Оберіть тип реєстрації, розширена або підписка?"
ADVANCED_INFO = "Розширена реєстрація дозволяє робити звернення та відслідковувати їх статус."
SUBSCRIPTION_INFO = "Підписка дає можливість оцінити роботу комунальних підприємств, користуватись довідковою інформацією і отримувати інформацію про проведення ремонтних робіт"

NEED_REGISTER = "Потрібно зареєструватись"
CALL_SUPPORT = "Зверніться до служби підтримки"

IS_REGISTER_ON_SITE = "Ви реєструвалися на сайті?"
IS_EMAIL_CONFIRMED = "Ви підтверджували свій e-mail?"
