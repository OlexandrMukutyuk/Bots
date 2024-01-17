from aiogram import types, Bot
from aiogram.fsm.context import FSMContext

from dto.guest import GuestIdDto, RateEnterpriseGuestDto
from handlers.common.enterprises import EnterprisesHandlers
from handlers.guest.cabinet.menu.handlers import give_cabinet_menu
from keyboards.inline.callbacks import EnterpriseCallbackFactory, EnterpriseRateCallbackFactory
from services.http_client import HttpGuestBot
from states import GuestRateEnterpriseStates


async def show_rate_for_enterprises(
    callback: types.CallbackQuery,
    callback_data: EnterpriseCallbackFactory,
    state: FSMContext,
    bot: Bot,
):
    user_data = await state.get_data()
    enterprises = await HttpGuestBot.get_enterprises(GuestIdDto(guest_id=user_data.get("GuestId")))

    return await EnterprisesHandlers.show_rate_for_enterprises(
        callback=callback,
        callback_data=callback_data,
        state=state,
        bot=bot,
        enterprises=enterprises,
        new_state=GuestRateEnterpriseStates.enterprise_selected,
    )


async def rate_enterprise(
    callback: types.CallbackQuery,
    callback_data: EnterpriseRateCallbackFactory,
    state: FSMContext,
    bot: Bot,
):
    guest_id = (await state.get_data()).get("GuestId")
    print(guest_id)
    rate = callback_data.rate
    enterprise_id = callback_data.enterprise_id

    await HttpGuestBot.rate_enterprise(
        RateEnterpriseGuestDto(guest_id=guest_id, enterprise_id=enterprise_id, rate=rate)
    )

    async def action():
        await give_cabinet_menu(state, bot=bot, chat_id=callback.from_user.id)

    return await EnterprisesHandlers.rate_enterprise(
        callback=callback, rate=rate, bot=bot, action=action
    )


# Back handlers


async def to_menu(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    async def action():
        await give_cabinet_menu(state, bot=bot, chat_id=callback.from_user.id)

    return await EnterprisesHandlers.to_menu(callback=callback, state=state, action=action)


async def to_enterprise_list(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    async def menu_callback():
        await give_cabinet_menu(state, bot=bot, chat_id=callback.from_user.id)

    async def get_enterprises():
        return await HttpGuestBot.get_enterprises(
            GuestIdDto(guest_id=(await state.get_data()).get("GuestId"))
        )

    return await EnterprisesHandlers.enterprises_list(
        state=state,
        menu_callback=menu_callback,
        get_enterprises=get_enterprises,
        new_state=GuestRateEnterpriseStates.showing_list,
        bot=bot,
        chat_id=callback.from_user.id,
        callback=callback,
    )
