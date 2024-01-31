import texts
from keyboards.constructor import KeyboardConstructor
from texts import TO_MENU
from viberio.types.messages.keyboard_message import Keyboard


def generate_archive_req_kb(requests: list[dict]) -> Keyboard:
    buttons = []

    for i, problem in enumerate(requests):
        if i == 20:
            break

        id = problem.get("Id")

        title = f'{problem.get("Reason")} #{id}'

        can_review = int(len(problem.get("Answers")) == 0)

        buttons.append({"Text": title, "ActionBody": f"REQUEST:{id}:{can_review}"})

    buttons.append({"Text": TO_MENU, "ActionBody": "to_menu"})

    return KeyboardConstructor.generate_kb(buttons, {"InputFieldState": "hidden"})


#
def confirm_archive_req_kb(req_id: int, can_review: bool) -> Keyboard:
    extra = []
    if can_review:
        pass
        # extra = [{"Text": "Залишити відгук та оцінити", "ActionBody": f"REVIEW:{req_id}"}]

    buttons = [
        *extra,
        {"Text": "Детальніше", "Columns": 3, "ActionBody": f"DETAILS:{req_id}"},
        {"Text": TO_MENU, "Columns": 3, "ActionBody": "to_menu"},
    ]

    return KeyboardConstructor.generate_kb(buttons, {"InputFieldState": "hidden"})


rate_request_kb = KeyboardConstructor.generate_kb(
    [
        {"Text": "⭐", "Columns": 3, "ActionBody": "1"},
        {"Text": "⭐⭐", "Columns": 3, "ActionBody": "2"},
        {"Text": "⭐⭐⭐", "Columns": 3, "ActionBody": "3"},
        {"Text": "⭐⭐⭐⭐", "Columns": 3, "ActionBody": "4"},
        {"Text": "⭐⭐⭐⭐⭐", "Columns": 3, "ActionBody": "5"},
        {"Text": texts.LATER, "Columns": 3},
    ],
    {"InputFieldState": "hidden"},
)
