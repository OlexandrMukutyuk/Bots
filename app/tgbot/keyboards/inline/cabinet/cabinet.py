from data import config
from keyboards.inline.consts import InlineConstructor

share_chatbot_kb = InlineConstructor.create_kb(
    actions=[
        {
            "text": "Поділитися",
            "url": f"https://t.me/share/url?url={config.BOT_URL}"
        },
        {
            "text": "До меню ↪️",
            "cb": "to_cabinet_menu"
        }
    ],
    schema=[2]
)
