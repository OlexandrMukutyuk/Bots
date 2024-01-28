from keyboards.constructor import KeyboardConstructor
from models import Gender
from texts import YES, NO, BACK, WITHOUT_FLAT


yes = KeyboardConstructor.generate_kb(
    [
        {"Text": YES, "Columns": 6, "Rows": 1},
    ]
)


no = KeyboardConstructor.generate_kb(
    [
        {"Text": NO, "Columns": 6, "Rows": 1},
    ]
)


yes_n_no = KeyboardConstructor.generate_kb(
    [
        {"Text": YES, "Columns": 3, "Rows": 1},
        {"Text": NO, "Columns": 3, "Rows": 1},
    ]
)


back_kb = KeyboardConstructor.generate_kb([{"Text": BACK}])

gender_keys = list(Gender.values_reversed.keys())

choose_gender_kb = KeyboardConstructor.generate_kb(
    [
        {
            "Text": gender_keys[0],
            "Columns": 3,
        },
        {
            "Text": gender_keys[1],
            "Columns": 3,
        },
        {
            "Text": gender_keys[2],
            "Columns": 6,
        },
    ],
    {"InputFieldState": "hidden"},
)


without_flat_kb = KeyboardConstructor.generate_kb([WITHOUT_FLAT])


without_flat_back_kb = KeyboardConstructor.generate_kb(
    [
        {"Text": BACK, "Columns": 3},
        {"Text": WITHOUT_FLAT, "Columns": 3},
    ]
)
