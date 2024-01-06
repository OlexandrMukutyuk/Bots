from aiogram import Router, F

from app.tgbot.handlers import validation
from app.tgbot.handlers.cabinet.create_request import handlers
from app.tgbot.keyboards.default.auth.register import change_street_text
from app.tgbot.keyboards.default.auth.start import yes_text, no_text
from app.tgbot.keyboards.default.cabinet.create_request import enough_text, back_text, no_need, main_menu_text, \
    manually_address_text, living_in_house
from app.tgbot.keyboards.inline.callbacks import ProblemCallbackFactory, StreetCallbackFactory
from app.tgbot.states.cabinet import CreateRequest, IssueReportStates


def prepare_router() -> Router:
    router = Router()

    # To main menu
    router.message.register(handlers.to_main_menu_reply, F.text == main_menu_text)
    router.callback_query.register(handlers.to_main_menu_inline, F.text == main_menu_text)

    # Choose problem
    router.inline_query.register(handlers.show_problems_list, CreateRequest.waiting_problem)
    router.message.register(handlers.save_problem_message, CreateRequest.waiting_problem, F.via_bot)
    router.callback_query.register(handlers.confirm_problem, ProblemCallbackFactory.filter(),
                                   CreateRequest.waiting_problem)
    router.callback_query.register(handlers.cancel_problem, CreateRequest.waiting_problem, F.data == 'cabinet_menu')

    # Choose reason

    router.inline_query.register(handlers.show_reasons_list, CreateRequest.waiting_reason)
    router.message.register(handlers.save_reason_message, CreateRequest.waiting_reason, F.via_bot)
    router.callback_query.register(handlers.confirm_reason, ProblemCallbackFactory.filter(),
                                   CreateRequest.waiting_reason)
    router.callback_query.register(handlers.cancel_reason, CreateRequest.waiting_reason, F.data == 'back')

    # Choose address
    router.message.register(handlers.flat_back, CreateRequest.waiting_address, F.text == back_text)
    router.message.register(handlers.request_on_my_house, CreateRequest.waiting_address, F.text == yes_text)
    router.message.register(handlers.manually_type_location, CreateRequest.waiting_address, F.text == no_text)

    # Manually Address

    router.message.register(handlers.manually_address_back, CreateRequest.is_address_manually, F.text == back_text)

    # Geo sharing
    router.message.register(handlers.location_by_geo, CreateRequest.is_address_manually, F.location)

    # Street choosing
    router.message.register(handlers.ask_for_street_name, CreateRequest.is_address_manually,
                            F.text == manually_address_text)

    router.message.register(handlers.choose_street, CreateRequest.waiting_street_typing, F.text.len() >= 3)

    router.inline_query.register(handlers.show_street_list, CreateRequest.waiting_street_selected)

    router.message.register(handlers.save_street_message, CreateRequest.waiting_street_selected, F.via_bot)

    router.callback_query.register(handlers.confirm_street, StreetCallbackFactory.filter(),
                                   CreateRequest.waiting_street_selected)

    # Choose house

    router.message.register(handlers.ask_for_street_name, CreateRequest.waiting_house, F.text == change_street_text)
    router.message.register(handlers.save_house, CreateRequest.waiting_house)

    # Choose flat

    router.message.register(handlers.flat_back, CreateRequest.waiting_flat, F.text == back_text)
    router.message.register(handlers.save_flat, CreateRequest.waiting_flat, F.text.isdigit())
    router.message.register(handlers.save_flat, CreateRequest.waiting_flat, F.text == living_in_house)

    # Choose comment

    router.message.register(handlers.comment_back, CreateRequest.waiting_comment, F.text == back_text)
    router.message.register(handlers.save_comment, CreateRequest.waiting_comment, F.text.len() >= 10)

    # Choose showing on site

    router.message.register(handlers.showing_status_back, CreateRequest.waiting_showing_status, F.text == back_text)
    router.message.register(handlers.save_showing_status, CreateRequest.waiting_showing_status,
                            F.text.in_([yes_text, no_text]))

    # Upload images

    router.message.register(handlers.saving_images_back, CreateRequest.waiting_images, F.text == back_text)
    router.message.register(handlers.saving_images, CreateRequest.waiting_images, F.photo)
    router.message.register(handlers.saving_images, CreateRequest.waiting_images, F.text.in_([no_need, enough_text]))

    # Showing all info
    router.message.register(handlers.showing_request_info, CreateRequest.waiting_confirm,
                            ~F.text.in_([yes_text, no_text]))

    # Confirm request

    router.message.register(handlers.confirm_request, CreateRequest.waiting_confirm, F.text == yes_text)
    router.message.register(handlers.to_main_menu_inline, CreateRequest.waiting_confirm, F.text == no_text)

    # Validation handlers
    router.message.register(validation.not_valid_text, IssueReportStates.waiting_issue_report)
    router.message.register(validation.not_valid_flat, CreateRequest.waiting_flat)
    router.message.register(validation.not_valid_comment, CreateRequest.waiting_comment)
    router.message.register(validation.not_valid_text, CreateRequest.waiting_showing_status)

    return router
