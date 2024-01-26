import texts
from keyboards.constructor import KeyboardConstructor

repairs_kb = KeyboardConstructor.generate_kb(
    [
        {"Text": texts.MY_ADDRESS, "ActionBody": "repairs_my_address"},
        {"Text": texts.OTHER_ADDRESS, "ActionBody": "repairs_other_address"},
        {"Text": texts.TO_MENU, "ActionBody": "to_menu"},
    ],
    {"InputFieldState": "hidden"},
)
