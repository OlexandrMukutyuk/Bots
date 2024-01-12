from aiogram import types, Bot
from aiogram.fsm.context import FSMContext

import texts
from handlers.cabinet.menu.handlers import give_cabinet_menu, send_edit_user_info
from handlers.common import generate_inline_street_list
from keyboards.default.auth.register import gender_dict
from keyboards.default.cabinet.edit_profile import edit_text, change_gender_kb, back_kb
from keyboards.inline.callbacks import StreetCallbackFactory
from keyboards.inline.streets import choose_street_kb
from services import http_client
from services.http_client import verify_address, fetch_streets
from states.cabinet import EditInfo
from utils.template_engine import render_template


async def handle_buttons(message: types.Message, state: FSMContext):
    button_type = message.text

    if button_type == edit_text["first_name_text"]:
        await state.set_state(EditInfo.waiting_first_name)
        await message.answer(text=texts.ASKING_FIRST_NAME, reply_markup=back_kb)
        return

    if button_type == edit_text["middle_name_text"]:
        await state.set_state(EditInfo.waiting_middle_name)
        await message.answer(text=texts.ASKING_MIDDLE_NAME, reply_markup=back_kb)
        return

    if button_type == edit_text["last_name_text"]:
        await state.set_state(EditInfo.waiting_last_name)
        await message.answer(text=render_template("asking/last_name.j2"), reply_markup=back_kb)
        return

    if button_type == edit_text["gender_text"]:
        await state.set_state(EditInfo.waiting_gender)
        await message.answer(
            text=render_template("asking/gender.j2"), reply_markup=change_gender_kb
        )
        return

    if button_type == edit_text["street_text"]:
        await state.set_state(EditInfo.waiting_street_typing)
        await message.answer(text=render_template("asking/stret.j2"), reply_markup=back_kb)
        return

    if button_type == edit_text["house_text"]:
        await state.set_state(EditInfo.waiting_house)
        await message.answer(text=render_template("asking/house.j2"), reply_markup=back_kb)
        return

    if button_type == edit_text["flat_text"]:
        await state.set_state(EditInfo.waiting_flat)
        await message.answer(text=render_template("asking/flat.j2"), reply_markup=back_kb)
        return


async def showing_user_info(message: types.Message, state: FSMContext):
    await send_edit_user_info(state, message=message)


# Edit names


async def edit_first_name(message: types.Message, state: FSMContext):
    first_name = message.text

    await state.update_data(FirstName=first_name)
    await state.set_state(EditInfo.waiting_acception)

    await send_edit_user_info(state, message=message)


async def edit_middle_name(message: types.Message, state: FSMContext):
    middle_name = message.text

    await state.update_data(MiddleName=middle_name)
    await state.set_state(EditInfo.waiting_acception)

    await send_edit_user_info(state, message=message)


async def edit_last_name(message: types.Message, state: FSMContext):
    last_name = message.text

    await state.update_data(LastName=last_name)
    await state.set_state(EditInfo.waiting_acception)

    await send_edit_user_info(state, message=message)


# Edit other


async def edit_street(message: types.Message, state: FSMContext):
    streets_data = await fetch_streets(message.text)

    if len(streets_data) == 0:
        await message.answer(render_template("services/not_found.j2"))
        return await message.answer(render_template("asking/street.j2"))

    await message.answer(
        text=render_template("user_info/pick_street.j2"), reply_markup=choose_street_kb
    )

    await state.update_data(Streets=streets_data)

    await state.set_state(EditInfo.waiting_street_selected)


async def show_street_list(callback: types.InlineQuery, state: FSMContext):
    data = await state.get_data()

    await generate_inline_street_list(data, callback)


async def confirm_street(
    callback: types.CallbackQuery, callback_data: StreetCallbackFactory, state: FSMContext, bot: Bot
):
    street_id = callback_data.street_id

    street = await http_client.get_street_by_id(street_id)

    await state.update_data(
        Streets=None,
        Street=street.get("name"),
        StreetId=street_id,
        CityId=callback_data.city_id,
    )

    await state.set_state(EditInfo.waiting_acception)

    await send_edit_user_info(state, bot=bot, chat_id=callback.from_user.id)

    return await callback.answer()


async def edit_house(message: types.Message, state: FSMContext):
    house = message.text
    street_id = (await state.get_data())["StreetId"]
    is_address_correct = await verify_address(street_id=street_id, house=house)

    if not is_address_correct:
        await message.answer(render_template("validation/house_not_found.j2"))
        await message.answer(text=render_template("asking/house.j2"), reply_markup=back_kb)
        return

    await state.update_data(House=house)
    await state.set_state(EditInfo.waiting_acception)

    await send_edit_user_info(state, message=message)


async def edit_flat(message: types.Message, state: FSMContext):
    flat = message.text

    await state.update_data(Flat=flat)
    await state.set_state(EditInfo.waiting_acception)

    await send_edit_user_info(state, message=message)


async def edit_gender(message: types.Message, state: FSMContext):
    gender = message.text

    if gender == gender_dict["other"]:
        gender = None
    elif gender == gender_dict["male"]:
        gender = "male"
    else:
        gender = "female"

    await state.update_data(Gender=gender)
    await state.set_state(EditInfo.waiting_acception)

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
