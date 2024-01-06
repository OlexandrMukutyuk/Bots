from keyboards.default.cabinet.create_request import main_menu_text
from keyboards.inline.callbacks import ProblemCallbackFactory
from keyboards.inline.consts import InlineConstructor

pick_problem_kb = InlineConstructor.create_kb(
    actions=[
        {
            "text": "Оберіть тему ↗️",
            "switch_inline_query_current_chat": 'problems_for_carousel'
        },
    ],
    schema=[1]
)

pick_reason_kb = InlineConstructor.create_kb(
    actions=[
        {
            "text": "Обрати підтему ↗️",
            "switch_inline_query_current_chat": 'reasons_for_carousel'
        },
    ],
    schema=[1]
)


def confirm_problem_kb(problem_id: int):
    return InlineConstructor.create_kb(
        actions=[
            {
                "text": "Вибрати ✅",
                "callback_data": ProblemCallbackFactory(problem_id=problem_id)
            },
            {
                "text": main_menu_text,
                "callback_data": 'cabinet_menu'
            }
        ],
        schema=[2]
    )


def confirm_reason_kb(reason_id: int):
    return InlineConstructor.create_kb(
        actions=[
            {
                "text": "Вибрати ✅",
                "callback_data": ProblemCallbackFactory(problem_id=reason_id)
            },
            {
                "text": "Назад",
                "callback_data": 'back'
            }
        ],
        schema=[2]
    )
