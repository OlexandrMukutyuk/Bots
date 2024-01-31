import texts
from keyboards.constructor import KeyboardConstructor
from texts import TO_MENU
from viberio.types.messages.keyboard_message import Keyboard


def generate_ref_info_kb(ref_info: list[dict]) -> Keyboard:
    buttons = []
    for i, item in enumerate(ref_info):
        if i == 19:
            break

        buttons.append(
            {
                "Text": item.get("Title"),
                "Columns": 3,
                "ActionBody": f"REF_INFO:{item.get('Id')}",
            }
        )

    if len(buttons) % 2 == 0:
        buttons.append(
            {"Text": TO_MENU, "Columns": 6, "ActionBody": "to_menu", "Color": texts.LIGHT}
        )
    else:
        buttons.append(
            {"Text": TO_MENU, "Columns": 3, "ActionBody": "to_menu", "Color": texts.LIGHT}
        )

    return KeyboardConstructor.generate_kb(buttons, {"InputFieldState": "hidden"})
