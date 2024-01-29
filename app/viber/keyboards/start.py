import random
import string

import texts
from keyboards.constructor import KeyboardConstructor
from texts import HELLO, AuthTypes, START_AGAIN, YES, NO, OTHER_MAIL

greeting_kb = KeyboardConstructor.generate_kb(
    buttons=[{"Text": HELLO, "Columns": 6, "Rows": 1}],
    options={"InputFieldState": "hidden", "HeightScale": None},
)

auth_types_kb = KeyboardConstructor.generate_kb(
    buttons=[
        {"Text": AuthTypes.advanced.value, "Columns": 3, "Rows": 1},
        {"Text": AuthTypes.guest.value, "Columns": 3, "Rows": 1},
    ],
    options={"InputFieldState": "hidden"},
)


is_register_on_site = KeyboardConstructor.generate_kb(
    buttons=[
        {"Text": YES, "Columns": 3},
        {"Text": NO, "Columns": 3},
        {"Text": OTHER_MAIL, "Columns": 6, "Color": texts.LIGHT},
    ],
    options={"InputFieldState": "hidden"},
)


start_again_kb = KeyboardConstructor.generate_kb([{"Text": START_AGAIN, "Columns": 6, "Rows": 1}])


def generate_random_string(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = "".join(random.choice(characters) for _ in range(length))
    return random_string


big_kb = KeyboardConstructor.generate_kb(
    [{"Text": f"{generate_random_string(20)}", "Columns": 3} for i in range(20)]
)
