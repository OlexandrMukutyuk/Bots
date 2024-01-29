import texts
from keyboards.constructor import KeyboardConstructor
from texts import (
    TO_MENU,
    BACK,
    TO_MAIN_MENU,
    YES,
    NO,
    CHANGE_STREET,
    LIVING_IN_HOUSE,
    NO_NEED,
    ENOUGH,
    SHARE_GEO,
    MANUALLY_ADDRESS,
)
from viberio.types.messages.keyboard_message import Keyboard


def generate_problem_kb(problems: list[dict]) -> Keyboard:
    buttons = []
    for i, problem in enumerate(problems):
        if i == 30:
            break

        id = problem.get("Id")
        name = problem.get("Name")

        buttons.append({"Text": name, "Columns": 3, "ActionBody": f"PROBLEM_ID:{id}"})

    buttons.append({"Text": TO_MENU, "ActionBody": "to_menu", "Color": texts.RED})

    return KeyboardConstructor.generate_kb(buttons, {"InputFieldState": "hidden"})


def generate_reasons_kb(problems: list[dict]) -> Keyboard:
    buttons = []
    for i, problem in enumerate(problems):
        if i == 30:
            break

        id = problem.get("Id")
        name = problem.get("Name")

        buttons.append({"Text": name, "Columns": 3, "ActionBody": f"PROBLEM_ID:{id}"})

    buttons.append({"Text": BACK, "ActionBody": "back", "Color": texts.RED})
    buttons.append({"Text": TO_MENU, "ActionBody": "to_menu", "Color": texts.RED})

    return KeyboardConstructor.generate_kb(buttons, {"InputFieldState": "hidden"})


request_back_and_main_kb = KeyboardConstructor.generate_kb(
    [
        {"Text": BACK, "Columns": 3, "Color": texts.RED},
        {"Text": TO_MAIN_MENU, "Columns": 3, "Color": texts.RED},
    ]
)

request_yes_no_kb = KeyboardConstructor.generate_kb(
    [
        {"Text": YES, "Columns": 3},
        {"Text": NO, "Columns": 3},
        {"Text": BACK, "Columns": 3, "Color": texts.RED},
        {"Text": TO_MAIN_MENU, "Columns": 3, "Color": texts.RED},
    ]
)


request_house_kb = KeyboardConstructor.generate_kb(
    [
        {"Text": CHANGE_STREET, "Columns": 3},
        {"Text": TO_MAIN_MENU, "Columns": 3, "Color": texts.RED},
    ]
)

request_flat_kb = KeyboardConstructor.generate_kb(
    [
        {"Text": LIVING_IN_HOUSE, "Columns": 6},
        {"Text": BACK, "Columns": 3, "Color": texts.RED},
        {"Text": TO_MAIN_MENU, "Columns": 3, "Color": texts.RED},
    ]
)

request_comment_kb = KeyboardConstructor.generate_kb(
    [
        {"Text": BACK, "Columns": 3, "Color": texts.RED},
        {"Text": TO_MAIN_MENU, "Columns": 3, "Color": texts.RED},
    ]
)

request_images_kb = KeyboardConstructor.generate_kb(
    [
        {"Text": NO_NEED, "Columns": 6},
        {"Text": BACK, "Columns": 3, "Color": texts.RED},
        {"Text": TO_MAIN_MENU, "Columns": 3, "Color": texts.RED},
    ]
)

request_enough_kb = KeyboardConstructor.generate_kb([ENOUGH])


request_manual_address_kb = KeyboardConstructor.generate_kb(
    [
        {"Text": MANUALLY_ADDRESS, "Columns": 3},
        {"Text": SHARE_GEO, "Columns": 3, "ActionType": "location-picker"},
        {"Text": BACK, "Columns": 3, "Color": texts.RED},
        {"Text": TO_MAIN_MENU, "Columns": 3, "Color": texts.RED},
    ]
)
