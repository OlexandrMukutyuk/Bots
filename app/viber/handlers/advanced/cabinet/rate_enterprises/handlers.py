from dto.chat_bot import UserIdDto, RateEnterpriseDto
from handlers.common.enterprises import EnterprisesHandlers
from handlers.common.helpers import full_cabinet_menu
from services.http_client import HttpChatBot
from states import FullRateEnterpriseStates
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.types import requests


async def show_rate_for_enterprises(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    user_data = await state.get_data()

    enterprises = await HttpChatBot.get_enterprises(UserIdDto(user_id=user_data.get("UserId")))

    return await EnterprisesHandlers.show_rate_for_enterprises(
        request=request,
        state=state,
        enterprises=enterprises,
        new_state=FullRateEnterpriseStates.enterprise_selected,
    )


async def rate_enterprise(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    user_id = (await state.get_data()).get("UserId")

    data_list = request.message.text.split(":")

    enterprise_id = int(data_list[1])
    rate = int(data_list[2])

    await HttpChatBot.rate_enterprise(
        RateEnterpriseDto(user_id=user_id, enterprise_id=enterprise_id, rate=rate)
    )

    async def action():
        await full_cabinet_menu(request, data)

    return await EnterprisesHandlers.rate_enterprise(request=request, rate=rate, action=action)


# Back handlers


async def to_enterprise_list(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    async def menu_callback():
        await full_cabinet_menu(request, data)

    async def get_enterprises():
        user_id = (await state.get_data()).get("UserId")
        return await HttpChatBot.get_enterprises(UserIdDto(user_id=user_id))

    return await EnterprisesHandlers.enterprises_list(
        request=request,
        state=state,
        get_enterprises=get_enterprises,
        new_state=FullRateEnterpriseStates.showing_list,
        menu_callback=menu_callback,
    )
