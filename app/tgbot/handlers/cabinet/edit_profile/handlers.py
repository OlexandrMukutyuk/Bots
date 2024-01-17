from aiogram import types, Bot
from aiogram.fsm.context import FSMContext

import texts
from handlers.cabinet.menu.handlers import give_cabinet_menu, send_edit_user_info
from handlers.common.house import HouseHandlers
from handlers.common.streets import StreetsHandlers
from keyboards.default.cabinet.edit_profile import edit_text, change_gender_kb, back_kb
from keyboards.inline.callbacks import StreetCallbackFactory
from models import Gender
from services import http_client
from states.advanced import EditInfoStates
from utils.template_engine import render_template


async def handle_buttons(message: types.Message, state: FSMContext):
    button_type = message.text

    if button_type == edit_text["first_name_text"]:
        await state.set_state(EditInfoStates.waiting_first_name)
        await message.answer(text=texts.ASKING_FIRST_NAME, reply_markup=back_kb)
        return

    if button_type == edit_text["middle_name_text"]:
        await state.set_state(EditInfoStates.waiting_middle_name)
        await message.answer(text=texts.ASKING_MIDDLE_NAME, reply_markup=back_kb)
        return

    if button_type == edit_text["last_name_text"]:
        await state.set_state(EditInfoStates.waiting_last_name)
        await message.answer(text=render_template("asking/last_name.j2"), reply_markup=back_kb)
        return

    if button_type == edit_text["gender_text"]:
        await state.set_state(EditInfoStates.waiting_gender)
        await message.answer(
            text=render_template("asking/gender.j2"), reply_markup=change_gender_kb
        )
        return

    if button_type == edit_text["street_text"]:
        await state.set_state(EditInfoStates.waiting_street_typing)
        await message.answer(text=render_template("asking/stret.j2"), reply_markup=back_kb)
        return

    if button_type == edit_text["house_text"]:
        await state.set_state(EditInfoStates.waiting_house)
        await message.answer(text=render_template("asking/house.j2"), reply_markup=back_kb)
        return

    if button_type == edit_text["flat_text"]:
        await state.set_state(EditInfoStates.waiting_flat)
        await message.answer(text=render_template("asking/flat.j2"), reply_markup=back_kb)
        return


async def showing_user_info(message: types.Message, state: FSMContext):
    await send_edit_user_info(state, message=message)


async def edit_first_name(message: types.Message, state: FSMContext):
    first_name = message.text

    await state.update_data(FirstName=first_name)
    await state.set_state(EditInfoStates.waiting_acceptation)

    await send_edit_user_info(state, message=message)


async def edit_middle_name(message: types.Message, state: FSMContext):
    middle_name = message.text

    await state.update_data(MiddleName=middle_name)
    await state.set_state(EditInfoStates.waiting_acceptation)

    await send_edit_user_info(state, message=message)


async def edit_last_name(message: types.Message, state: FSMContext):
    last_name = message.text

    await state.update_data(LastName=last_name)
    await state.set_state(EditInfoStates.waiting_acceptation)

    await send_edit_user_info(state, message=message)


# Edit other


async def edit_street(message: types.Message, state: FSMContext, bot: Bot):
    return await StreetsHandlers.choose_street(
        message=message, state=state, new_state=EditInfoStates.waiting_street_selected, bot=bot
    )


async def show_street_list(callback: types.InlineQuery, state: FSMContext):
    data = await state.get_data()

    return await StreetsHandlers.inline_list(callback, data)


async def confirm_street(
    callback: types.CallbackQuery, callback_data: StreetCallbackFactory, state: FSMContext, bot: Bot
):
    async def action():
        await state.set_state(EditInfoStates.waiting_acceptation)
        await send_edit_user_info(state, bot=bot, chat_id=callback.from_user.id)

    await StreetsHandlers.confirm_street(
        callback=callback, callback_data=callback_data, state=state, action=action, bot=bot
    )


async def edit_house(message: types.Message, state: FSMContext):
    async def callback():
        await send_edit_user_info(state, message=message)

    return HouseHandlers.change_house(
        message=message,
        state=state,
        new_state=EditInfoStates.waiting_acceptation,
        callback=callback,
    )


async def edit_flat(message: types.Message, state: FSMContext):
    flat = message.text

    await state.update_data(Flat=flat)
    await state.set_state(EditInfoStates.waiting_acceptation)

    await send_edit_user_info(state, message=message)


async def edit_gender(message: types.Message, state: FSMContext):
    gender = Gender.get_key(message.text)

    await state.update_data(Gender=gender)
    await state.set_state(EditInfoStates.waiting_acceptation)

    await send_edit_user_info(state, message=message)


async def confirm(message: types.Message, state: FSMContext):
    user_data = await state.get_data()

    await http_client.update_profile(
        {
            "UserId": user_data.get("UserId"),
            "Phone": user_data.get("Phone"),
            "CityId": user_data.get("CityId"),
            "StreetId": user_data.get("StreetId"),
            "House": user_data.get("House"),
            "Flat": user_data.get("Flat"),
            "FirstName": user_data.get("FirstName"),
            "MiddleName": user_data.get("MiddleName"),
            "LastName": user_data.get("LastName"),
            "Gender": user_data.get("Gender"),
        }
    )

    await message.answer(render_template("user_info/edited_successfully.j2"))

    return await give_cabinet_menu(state, message=message)
