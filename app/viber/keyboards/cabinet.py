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
        {"Text": guest_menu_text["repairs"], "Columns": 3, "Rows": 1},
        {"Text": guest_menu_text["change_info"], "Columns": 3, "Rows": 1},
        {
            "Text": guest_menu_text["share_chatbot"],
            "Columns": 3,
            "Rows": 1,
            "InternalBrowser": True,
        },
        {"Text": guest_menu_text["reference_info"], "Columns": 3, "Rows": 1},
        {"Text": guest_menu_text["review_enterprises"], "Columns": 3, "Rows": 1},
        {"Text": guest_menu_text["full_registration"], "Columns": 3, "Rows": 1},
    ],
    {"InputFieldState": "hidden"},
)


full_registration_kb = KeyboardConstructor.generate_kb(
    [
        {"Text": START_FULL_REGISTRATION},
        {"Text": GO_BACK},
    ]
)
