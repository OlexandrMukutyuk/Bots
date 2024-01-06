from aiogram import types, Bot
from aiogram.fsm.context import FSMContext

from handlers.cabinet.menu.handlers import give_cabinet_menu
from keyboards.inline.cabinet.rate_enterprises import enterprises_rates_kb, enterprises_list_kb
from keyboards.inline.callbacks import EnterpriseCallbackFactory, EnterpriseRateCallbackFactory
from services import http_client
from states.cabinet import RateEnterprise


async def show_rate_for_enterprises(
        callback: types.CallbackQuery,
        callback_data: EnterpriseCallbackFactory,
        state: FSMContext,
        bot: Bot
):
    user_data = await state.get_data()
    enterprise_id = callback_data.enterprise_id

    message_id = callback.message.message_id

    enterprises = await http_client.get_enterprises(user_id=user_data.get('UserId'))

    enterprise_name = ''
    for enterprise in enterprises:
        if enterprise.get('Id') == enterprise_id:
            enterprise_name = enterprise.get('Name')

    chat_id = callback.from_user.id

    await state.set_state(RateEnterprise.enterprise_selected)

    await bot.edit_message_text(
        text=f"Будь ласка, оцініть підприємство {enterprise_name}",
        message_id=message_id,
        chat_id=chat_id,
        reply_markup=enterprises_rates_kb(enterprise_id=enterprise_id)
    )


async def rate_enterprise(
        callback: types.CallbackQuery,
        callback_data: EnterpriseRateCallbackFactory,
        state: FSMContext,
        bot: Bot
):
    user_id = (await state.get_data()).get('UserId')
    chat_id = callback.from_user.id

    rate = callback_data.rate
    enterprise_id = callback_data.enterprise_id

    status = await http_client.rate_enterprise({
        "UserId": user_id,
        "KpId": enterprise_id,
        "Rate": rate,
    })

    await bot.send_message(chat_id=chat_id, text=f"Оцінка {rate} ⭐️")
    await bot.send_message(chat_id=chat_id, text='Ваша оцінка відправлена успішно')

    await callback.message.delete()

    return await give_cabinet_menu(state, bot=bot, chat_id=chat_id)


# Back handlers

async def to_menu(
        callback: types.CallbackQuery,
        state: FSMContext,
        bot: Bot
):
    chat_id = callback.from_user.id

    await callback.message.delete()

    return await give_cabinet_menu(state, bot=bot, chat_id=chat_id)


async def to_enterprise_list(
        callback: types.CallbackQuery,
        state: FSMContext,
        bot: Bot
):
    user_data = await state.get_data()
    chat_id = callback.from_user.id

    message_id = callback.message.message_id

    enterprises = await http_client.get_enterprises(user_id=user_data.get('UserId'))

    allowed_to_rate = list(filter(lambda item: item.get('CanVote'), enterprises))

    if len(allowed_to_rate) == 0:
        await bot.send_message(chat_id=chat_id, text='Наразі для вас немає доступних для оцінювання підприємств')
        return await give_cabinet_menu(state, bot=bot, chat_id=chat_id)

    await bot.edit_message_text(
        text='Оберіть підприємство, яке ви хотіли би оцінити ⭐️',
        message_id=message_id,
        chat_id=chat_id,
        reply_markup=enterprises_list_kb(allowed_to_rate)
    )

    await state.set_state(RateEnterprise.showing_list)
