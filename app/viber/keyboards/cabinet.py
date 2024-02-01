import texts
from data import config
from keyboards.constructor import KeyboardConstructor
from texts import START_FULL_REGISTRATION, GO_BACK

guest_menu_text = {
    "repairs": "Ремонтні роботи ⚒️️",
    "change_info": "Змінити дані 🔄",
    "share_chatbot": "Поділитися чат-ботом 🤝️",
    "reference_info": "Довідкова інформація ℹ️",
    "review_enterprises": "Оцінити роботу підприємств міста ⭐",
    "full_registration": "Пройти повну реєстрацію ✍",
}


guest_menu_kb = KeyboardConstructor.generate_kb(
    [
        # {"Text": guest_menu_text["repairs"], "Columns": 3, "Rows": 1},
        {"Text": guest_menu_text["change_info"], "Columns": 3, "Rows": 1},
        {
            "Text": guest_menu_text["share_chatbot"],
            "ActionType": "open-url",
            "ActionBody": f"viber://forward?text={config.BOT_URL}",
            "Columns": 3,
        },
        {"Text": guest_menu_text["reference_info"], "Columns": 3, "Rows": 1},
        # {"Text": guest_menu_text["review_enterprises"], "Columns": 3, "Rows": 1},
        {"Text": guest_menu_text["full_registration"], "Columns": 3, "Rows": 1},
    ],
    {"InputFieldState": "hidden"},
)


full_registration_kb = KeyboardConstructor.generate_kb(
    [
        {"Text": START_FULL_REGISTRATION, "Color": texts.RED},
        {"Text": GO_BACK},
    ]
)


cabinet_menu_text = {
    "create_request": "Створити звернення ✍",
    "actual_requests": "Актуальні звернення 📝",
    "history_requests": "Історія звернень 📚",
    "repairs": "Ремонтні роботи ⚒️️",
    "change_user_info": "Змінити дані 🔄",
    "share_chatbot": "Поділитися чат-ботом 🤝️",
    "report_issue": "Повідомити про технічні негаразди ⚙️",
    "reference_info": "Довідкова інформація ℹ️",
    "review_enterprises": "Оцінити роботу підприємств міста ⭐",
}


cabinet_menu_kb = KeyboardConstructor.generate_kb(
    [
        {"Text": cabinet_menu_text["create_request"], "Columns": 3, "Rows": 1},
        {"Text": cabinet_menu_text["actual_requests"], "Columns": 3, "Rows": 1},
        {"Text": cabinet_menu_text["history_requests"], "Columns": 3, "Rows": 1},
        # {"Text": cabinet_menu_text["repairs"], "Columns": 3, "Rows": 1},
        {"Text": cabinet_menu_text["change_user_info"], "Columns": 3, "Rows": 1},
        {
            "Text": cabinet_menu_text["share_chatbot"],
            "ActionType": "open-url",
            "ActionBody": f"viber://forward?text={config.BOT_URL}",
            "Columns": 3,
        },
        {"Text": cabinet_menu_text["reference_info"], "Columns": 3, "Rows": 1},
        {"Text": cabinet_menu_text["report_issue"], "Columns": 6, "Rows": 1},
        # {"Text": cabinet_menu_text["review_enterprises"], "Columns": 6, "Rows": 1},
    ],
    {"InputFieldState": "hidden"},
)
