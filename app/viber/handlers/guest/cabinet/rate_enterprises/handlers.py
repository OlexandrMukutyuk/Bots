from dto.guest import GuestIdDto, RateEnterpriseGuestDto
from handlers.common.enterprises import EnterprisesHandlers
from handlers.guest.cabinet.menu.handlers import show_cabinet_menu
from services.http_client import HttpGuestBot
from states import GuestRateEnterpriseStates
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.types import requests


async def show_rate_for_enterprises(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    user_data = await state.get_data()
    enterprises = await HttpGuestBot.get_enterprises(GuestIdDto(guest_id=user_data.get("GuestId")))

    return await EnterprisesHandlers.show_rate_for_enterprises(
        request=request,
        state=state,
        enterprises=enterprises,
        new_state=GuestRateEnterpriseStates.enterprise_selected,
    )


async def rate_enterprise(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    guest_id = (await state.get_data()).get("GuestId")

    data_list = request.message.text.split(":")

    enterprise_id = int(data_list[1])
    rate = int(data_list[2])

    await HttpGuestBot.rate_enterprise(
        RateEnterpriseGuestDto(guest_id=guest_id, enterprise_id=enterprise_id, rate=rate)
    )

    async def action():
        await show_cabinet_menu(request, data)

    return await EnterprisesHandlers.rate_enterprise(request=request, rate=rate, action=action)


# Back handlers


async def to_menu(request: requests.ViberMessageRequest, data: dict):
    await show_cabinet_menu(request, data)


async def to_enterprise_list(request: requests.ViberMessageRequest, data: dict):
    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    async def menu_callback():
        await show_cabinet_menu(request, data)

    async def get_enterprises():
        return await HttpGuestBot.get_enterprises(
            GuestIdDto(guest_id=(await state.get_data()).get("GuestId"))
        )

    return await EnterprisesHandlers.enterprises_list(
        request=request,
        state=state,
        get_enterprises=get_enterprises,
        new_state=GuestRateEnterpriseStates.showing_list,
        menu_callback=menu_callback,
    )
