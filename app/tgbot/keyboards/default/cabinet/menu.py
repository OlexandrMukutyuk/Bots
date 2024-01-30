from keyboards.default.consts import DefaultConstructor

cabinet_menu_text = {
    "create_request": "Створити звернення ✍",
    "actual_requests": "Актуальні звернення 📝",
    "history_requests": "Історія звернень 📚",
    # "repairs": "Ремонтні роботи ⚒️️",
    "change_user_info": "Змінити дані 🔄",
    "share_chatbot": "Поділитися чат-ботом 🤝️",
    "report_issue": "Повідомити про технічні негарди ⚙️",
    "reference_info": "Довідкова інформація ℹ️",
    # "review_enterprises": "Оцінити роботу підприємств міста ⭐",
}

cabinet_menu_kb = DefaultConstructor.create_kb(
    actions=[item for item in cabinet_menu_text.values()], schema=[2, 2, 2, 1]
    # actions=[item for item in cabinet_menu_text.values()], schema=[2, 2, 2, 2, 1]
)
