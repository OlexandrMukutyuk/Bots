import texts
from keyboards.inline.consts import InlineConstructor

repairs_kb = InlineConstructor.create_kb(
    actions=[
        {
            "text": texts.MY_ADDRESS,
            "cb": "repairs_my_address"
        },
        {
            "text": texts.OTHER_ADDRESS,
            "cb": "repairs_other_address"
        },
        {
            "text": texts.TO_MENU,
            "cb": "to_menu"
        }
    ],
    schema=[1, 1, 1]
)
