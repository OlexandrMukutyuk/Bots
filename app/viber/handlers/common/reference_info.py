from asyncio import sleep
from typing import Optional

import texts
from dto.chat_bot import ParentIdDto
from keyboards.reference_info import generate_ref_info_kb
from services.database import update_last_message
from services.http_client import HttpChatBot
from utils.template_engine import render_template
from viber import viber
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.fsm.context import FSMContext
from viberio.fsm.states import State
from viberio.types import requests, messages


class ReferenceInfoHandlers:
    @staticmethod
    async def load_menu(
        request: requests.ViberMessageRequest,
        state: FSMContext,
        parent_id: Optional[int],
        new_state: Optional[State],
    ):
        sender_id = request.sender.id
        ref_info = await HttpChatBot.get_information(ParentIdDto(parent_id=parent_id))

        await state.update_data(ReferenceInfo=ref_info)

        if new_state:
            await state.set_state(new_state)

        kb = generate_ref_info_kb(ref_info)

        await update_last_message(sender_id, texts.ASKING_REF_INFO, kb)

        await viber.send_messages(
            sender_id,
            messages.KeyboardMessage(
                text=texts.ASKING_REF_INFO,
                keyboard=kb,
                min_api_version="3",
            ),
        )

    @staticmethod
    async def show_info(
        request: requests.ViberMessageRequest,
        data: dict,
    ):
        dp_ = Dispatcher.get_current()
        state = dp_.current_state(request)

        data_info = request.message.text.split(":")
        current_info_id = int(data_info[1])

        ref_info = (await state.get_data()).get("ReferenceInfo")

        target_info = next((info for info in ref_info if info.get("Id") == current_info_id), None)

        if target_info.get("Description") is None:
            await ReferenceInfoHandlers.load_menu(
                request=request, state=state, parent_id=current_info_id, new_state=None
            )

        else:
            sender_id = request.sender.id

            await viber.send_message(
                sender_id,
                messages.TextMessage(text=render_template("show_ref_info.j2", info=target_info)),
            )

            await sleep(0.2)
            kb = generate_ref_info_kb(ref_info)

            await update_last_message(sender_id, texts.ASKING_REF_INFO, kb)

            await viber.send_message(
                sender_id,
                messages.KeyboardMessage(
                    text=texts.ASKING_REF_INFO,
                    keyboard=kb,
                    min_api_version="3",
                ),
            )
