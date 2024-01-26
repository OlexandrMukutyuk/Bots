from typing import Callable

import texts
from keyboards.enterprises import enterprises_list_kb, enterprises_rates_kb
from utils.template_engine import render_template
from viber import viber
from viberio.fsm.context import FSMContext
from viberio.fsm.states import State
from viberio.types import requests, messages


class EnterprisesHandlers:
    @staticmethod
    async def enterprises_list(
        request: requests.ViberMessageRequest,
        state: FSMContext,
        get_enterprises: Callable,
        new_state: State,
        menu_callback: Callable,
    ):
        sender_id = request.sender.id

        enterprises = await get_enterprises()
        allowed_to_rate = list(filter(lambda item: item.get("CanVote"), enterprises))

        if len(allowed_to_rate) == 0:
            await viber.send_message(
                sender_id, messages.TextMessage(text=texts.NO_ENTERPRISES_TO_RATE)
            )
            return await menu_callback()

        await viber.send_message(
            sender_id,
            messages.KeyboardMessage(
                text=texts.ASKING_ENTERPRISE,
                keyboard=enterprises_list_kb(allowed_to_rate),
                min_api_version="3",
            ),
        )

        await state.set_state(new_state)

    @staticmethod
    async def show_rate_for_enterprises(
        request: requests.ViberMessageRequest,
        state: FSMContext,
        enterprises: list[dict],
        new_state: State,
    ):
        text = request.message.text
        enterprise_id = int(text.split(":")[1])

        enterprise_name = ""
        for enterprise in enterprises:
            if enterprise.get("Id") == enterprise_id:
                enterprise_name = enterprise.get("Name")

        await state.set_state(new_state)

        await viber.send_message(
            request.sender.id,
            messages.KeyboardMessage(
                text=render_template("rate_enterprise.j2", title=enterprise_name),
                keyboard=enterprises_rates_kb(enterprise_id=enterprise_id),
                min_api_version="3",
            ),
        )

    @staticmethod
    async def rate_enterprise(request: requests.ViberMessageRequest, rate: int, action: Callable):
        await viber.send_messages(
            request.sender.id,
            [
                messages.TextMessage(text=f"Оцінка {rate} ⭐️"),
                messages.TextMessage(text="Ваша оцінка відправлена успішно"),
            ],
        )

        return await action()
