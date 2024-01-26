from keyboards.constructor import KeyboardConstructor
from texts import BACK
from viberio.types.messages.keyboard_message import Keyboard


def enterprises_list_kb(enterprises: list[dict]) -> Keyboard:
    buttons = []
    for i, enterprise in enumerate(enterprises):
        if i == 19:
            break

        buttons.append(
            {"Text": enterprise.get("Name"), "ActionBody": f"ENTERPRISE_ID:{enterprise.get('Id')}"}
        )

    buttons.append({"Text": BACK, "ActionBody": "back"})

    return KeyboardConstructor.generate_kb(buttons, {"InputFieldState": "hidden"})


def enterprises_rates_kb(enterprise_id: int):
    buttons = []

    rates = [5, 4, 3, 2, 1]

    for rate in rates:
        buttons.append(
            {
                "Text": f"{rate} ⭐",
                "Columns": 3,
                "ActionBody": f"ENTERPRISE_RATE:{enterprise_id}:{rate}",
            }
        )

    buttons.append({"Text": BACK, "Columns": 3, "ActionBody": "back"})

    return KeyboardConstructor.generate_kb(buttons, {"InputFieldState": "hidden"})
