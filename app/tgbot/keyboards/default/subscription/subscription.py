from keyboards.default.consts import DefaultConstructor

subscription_menu_text = {
    "repairs": "Ремонтні роботи ⚒️️",
    "change_user_info": "Змінити дані 🔄",
    "share_chatbot": "Поділитися чат-ботом 🤝️",
    "reference_info": "Довідкова інформація ℹ️",
    "review_enterprises": "Оцінити роботу підприємств міста ⭐",
    "full_registration": "Пройти повну реєстрацію ✍",
}


subscription_menu_kb = DefaultConstructor.create_kb(
    actions=[item for item in subscription_menu_text.values()], schema=[2, 2, 2]
)
