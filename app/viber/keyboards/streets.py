from keyboards.constructor import KeyboardConstructor
from texts import CHANGE_STREET
from viberio.types.messages.keyboard_message import Keyboard


def streets_keyboard(streets: list[dict]) -> Keyboard:
    buttons = []
    for i, street in enumerate(streets):
        if i == 20:
            break

        street_id = street["Id"]
        city_id = street["CityId"]

        city = street["City"]
        title = street["Type"] + " " + street["Name"] + f"\n{city}"

        buttons.append(
            {"Text": title, "Columns": 3, "ActionBody": f"STREET_ID:{street_id}:{city_id}"}
        )

    return KeyboardConstructor.generate_kb(buttons, {"InputFieldState": "hidden"})


change_street_kb = KeyboardConstructor.generate_kb([CHANGE_STREET])
