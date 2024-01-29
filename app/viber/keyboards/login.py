import texts
from keyboards.constructor import KeyboardConstructor
from texts import OTHER_MAIL


other_email_kb = KeyboardConstructor.generate_kb([{"Text": OTHER_MAIL, "Color": texts.LIGHT}])
