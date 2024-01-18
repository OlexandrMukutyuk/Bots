from keyboards.default.consts import DefaultConstructor
from texts import HELLO, OTHER_MAIL, NO, YES, START_AGAIN, AuthTypes

greeting_kb = DefaultConstructor.create_kb(actions=[HELLO], schema=[1])

auth_types_kb = DefaultConstructor.create_kb(actions=[*AuthTypes.values()], schema=[2])

is_register_on_site = DefaultConstructor.create_kb(actions=[YES, NO, OTHER_MAIL], schema=[2, 1])

start_again_kb = DefaultConstructor.create_kb(actions=[START_AGAIN], schema=[1])
