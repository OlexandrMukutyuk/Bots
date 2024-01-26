from keyboards.constructor import KeyboardConstructor
from texts import SHARE_CONTACT


phone_share_kb = KeyboardConstructor.generate_kb(
    [
        {"Text": SHARE_CONTACT, "ActionType": "share-phone", "Columns": 6, "Rows": 1},
    ]
)
