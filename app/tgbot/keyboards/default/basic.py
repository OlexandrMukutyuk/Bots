from keyboards.default.start import no_text, yes_text
from .consts import DefaultConstructor

yes = DefaultConstructor.create_kb(actions=[yes_text], schema=[1])

no = DefaultConstructor.create_kb(actions=[no_text], schema=[1])

yes_n_no = DefaultConstructor.create_kb(actions=[yes_text, no_text], schema=[2])
