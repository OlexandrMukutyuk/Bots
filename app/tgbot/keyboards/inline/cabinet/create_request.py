from keyboards.inline.callbacks import ProblemCallbackFactory
from keyboards.inline.consts import InlineConstructor
from texts.keyboards import TO_MAIN_MENU, BACK, CHOOSE_PROBLEM, CHOOSE_REASON, CHOOSE

pick_problem_kb = InlineConstructor.create_kb(
    actions=[
        {"text": CHOOSE_PROBLEM, "switch_inline_query_current_chat": "problems_for_carousel"},
    ],
    schema=[1],
)

pick_reason_kb = InlineConstructor.create_kb(
    actions=[
        {"text": CHOOSE_REASON, "switch_inline_query_current_chat": "reasons_for_carousel"},
    ],
    schema=[1],
)


def confirm_problem_kb(problem_id: int):
    return InlineConstructor.create_kb(
        actions=[
            {"text": CHOOSE, "callback_data": ProblemCallbackFactory(problem_id=problem_id)},
            {"text": TO_MAIN_MENU, "callback_data": "cabinet_menu"},
        ],
        schema=[2],
    )


def confirm_reason_kb(reason_id: int):
    return InlineConstructor.create_kb(
        actions=[
            {"text": CHOOSE, "callback_data": ProblemCallbackFactory(problem_id=reason_id)},
            {"text": BACK, "callback_data": "back"},
        ],
        schema=[2],
    )
