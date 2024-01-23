from aiogram.filters.callback_data import CallbackData


class StreetCallbackFactory(CallbackData, prefix="user_street"):
    street_id: int
    city_id: int


class ProblemCallbackFactory(CallbackData, prefix="problem"):
    problem_id: int


class EnterpriseCallbackFactory(CallbackData, prefix="enterprise"):
    enterprise_id: int


class EnterpriseRateCallbackFactory(CallbackData, prefix="enterprise_rate"):
    rate: int
    enterprise_id: int


class ArchiveReqCallbackFactory(CallbackData, prefix="archive_req"):
    req_id: int
    review: bool


class ReferenceInfoCallbackFactory(CallbackData, prefix="ref_info"):
    id: int
