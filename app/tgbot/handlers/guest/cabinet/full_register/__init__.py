from aiogram import Router, F

import texts
from handlers.common.helpers import Handler
from handlers.guest.cabinet.full_register import handlers
from handlers.guest.cabinet.menu import handlers as menu
from states import GuestFullRegisterStates


def prepare_router() -> Router:
    router = Router()

    message_list = [
        Handler(
            menu.show_cabinet_menu,
            [GuestFullRegisterStates.waiting_answer, F.text == texts.GO_BACK],
        ),
        Handler(
            handlers.begin_full_registration,
            [GuestFullRegisterStates.waiting_answer, F.text == texts.START_FULL_REGISTRATION],
        ),
        Handler(menu.full_registration, [GuestFullRegisterStates.waiting_answer]),
    ]

    for message in message_list:
        router.message.register(message.handler, *message.filters)

    return router
