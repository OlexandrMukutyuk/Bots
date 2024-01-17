from keyboards.default.consts import DefaultConstructor
from texts.keyboards import START_FULL_REGISTRATION, GO_BACK

guest_menu_text = {
    "repairs": "Ремонтні роботи ⚒️️",
    "change_info": "Змінити дані 🔄",
    "share_chatbot": "Поділитися чат-ботом 🤝️",
    "reference_info": "Довідкова інформація ℹ️",
    "review_enterprises": "Оцінити роботу підприємств міста ⭐",
    "full_registration": "Пройти повну реєстрацію ✍",
}


subscription_menu_kb = DefaultConstructor.create_kb(
    actions=[item for item in guest_menu_text.values()], schema=[2, 2, 2]
)


full_registration_kb = DefaultConstructor.create_kb(
    actions=[START_FULL_REGISTRATION, GO_BACK], schema=[2]
)
