from keyboards.inline.callbacks import ArchiveReqCallbackFactory
from keyboards.inline.consts import InlineConstructor

to_menu = "До меню"

pick_archive_req_kb = InlineConstructor.create_kb(
    actions=[
        {
            "text": "Обрати звернення ↗️",
            "switch_inline_query_current_chat": 'archived_for_carousel'
        },
    ],
    schema=[1]
)


def confirm_archive_req_kb(req_id: int, can_review: bool):
    actions = [
        {
            "text": "Детальніше",
            "callback_data": ArchiveReqCallbackFactory(req_id=req_id, review=False)
        },
        {
            "text": to_menu,
            "callback_data": 'cabinet_menu'
        }
    ]

    schema = [2]

    if can_review:
        pass
        # actions = [
        #     {
        #         "text": "Залишити відгук та оцінити",
        #         "callback_data": ArchiveReqCallbackFactory(req_id=req_id, review=True)
        #     },
        #     *actions
        # ]
        # schema = [1] + schema

    return InlineConstructor.create_kb(
        actions=actions,
        schema=schema
    )
