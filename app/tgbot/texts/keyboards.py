from enum import Enum

SHARE_CONTACT = "Поділитись телефоном"
AGREEMENT = "Погоджуюсь ✅"
WITHOUT_FLAT = "Передавати номер квартири не потрібно"
CHANGE_STREET = "Змінити вулицю"

TO_MAIN_MENU = "В головне меню"
TO_MENU = "До меню 🔙"
BACK = "Назад 🔙"
LIVING_IN_HOUSE = "Живу у домі"
NO_NEED = "Не потрібно ❌"
ENOUGH = "Достатньо ✅"
MANUALLY_ADDRESS = "Вписати адресу"
SHARE_GEO = "Поділитися геолокацією"

CHOOSE_PROBLEM = "Оберіть тему ↗️"
CHOOSE_REASON = "Обрати підтему ↗️"
CHOOSE = "Обрати "

START_FULL_REGISTRATION = "Розпочати повну реєстрацію 👇"
GO_BACK = "Повернутись назад  🔙"

HELLO = "Привіт! 👋"
YES = "Так ✅"
NO = "Ні ❌"
OTHER_MAIL = "Інша пошта 🔁"
START_AGAIN = "Почати спочатку 🔁"

MY_ADDRESS = 'За моєю адресою 👇'
OTHER_ADDRESS = 'ЗА іншою адресою ⬇️'


class AuthTypes(Enum):
    guest = "Підписка"
    advanced = "Розширена"

    @staticmethod
    def values():
        return [i.value for i in AuthTypes]
