from texts import YES, NO
from .consts import DefaultConstructor

yes = DefaultConstructor.create_kb(actions=[YES], schema=[1])

no = DefaultConstructor.create_kb(actions=[NO], schema=[1])

yes_n_no = DefaultConstructor.create_kb(actions=[YES, NO], schema=[2])
