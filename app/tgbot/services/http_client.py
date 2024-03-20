import json

import aiohttp
from data.config import SERVER_BASE_URL, SERVER_BASE_SERVICE, SERVER_GUEST_SERVICE, SERVER_USER, SERVER_PASSWORD
from dto import AbstractDto
from dto.chat_bot import (
    SearchDto,
    VerifyAddressDto,
    CheckEmailDto,
    EmailDto,
    UserIdDto,
    ReportIssueDto,
    ProblemIdDto,
    AddressByGeoDto,
    CreateRequestDto,
    RateRequestDto,
    UpdateUserDto,
    ChooseRegionDto,
    RateEnterpriseDto, ParentIdDto, GenerateTokenDto, PhoneDto,
)
from dto.chat_bot.register import RegisterDto
from dto.chat_bot.repairs import RepairsDto
from dto.guest import UpdateGuestDto, GuestIdDto, RegisterGuestDto, RateEnterpriseGuestDto
from dto.guest.repairs_guest import RepairsGuestDto


class HttpClient:
    access_token = ''

    @staticmethod
    async def make_request(path: str, service: str, dto: AbstractDto):
        res = await HttpClient.post(data=dto.to_payload(), path=path, service=service)

        if res.get('Code') == 103 and res.get("Message") == 'Token is not valid':
            await HttpClient.update_token()
            res = await HttpClient.post(data=dto.to_payload(), path=path, service=service)

        return res

    @staticmethod
    async def update_token():
        dto = GenerateTokenDto(SERVER_USER, SERVER_PASSWORD)

        res = await HttpClient.make_request('/GetToken', SERVER_BASE_SERVICE, dto)

        token = res.get('Token')

        HttpClient.access_token = token

    @staticmethod
    async def post(data: dict, **kwargs) -> dict:
        encoded_data = json.dumps(data)

        full_url: str = kwargs.get("full_url")

        headers = {
            "Token": HttpClient.access_token,
            "Content-Type": "application/json"
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            if not full_url:
                full_url = f'{SERVER_BASE_URL}/{kwargs.get("service")}{kwargs.get("path")}'

            async with session.post(url=full_url, data=encoded_data, ssl=False) as resp:
                return await resp.json()


class HttpInfoClient(HttpClient):
    @staticmethod
    async def get_street_by_id(street_id: int) -> dict:
        response = await HttpInfoClient.post(
            data={"streetid": street_id},
            full_url=f"{SERVER_BASE_URL}/Services/Dictionary/json/getstreetbyid",
        )

        return response.get("list")[0]

    @staticmethod
    async def get_city_by_id(city_id: int) -> dict:
        response = await HttpInfoClient.post(
            data={"cityid": city_id},
            full_url=f"{SERVER_BASE_URL}/Services/Dictionary/json/getcities",
        )

        return response.get("list")[0]


class HttpGuestBot(HttpClient):
    BASE_SERVICE = SERVER_GUEST_SERVICE

    @staticmethod
    async def request(path: str, dto: AbstractDto):
        return await HttpClient.make_request(path, HttpGuestBot.BASE_SERVICE, dto)

    @staticmethod
    async def register(dto: RegisterGuestDto):
        return await HttpGuestBot.request("/Register", dto)

    @staticmethod
    async def update_data(dto: UpdateGuestDto):
        return await HttpGuestBot.request("/Update", dto)

    @staticmethod
    async def get_enterprises(dto: GuestIdDto):
        data = await HttpGuestBot.request("/GetKps", dto)

        return data.get("Items")

    @staticmethod
    async def rate_enterprise(dto: RateEnterpriseGuestDto):
        return await HttpGuestBot.request("/SaveKpRate", dto)

    @staticmethod
    async def get_repairs(dto: RepairsGuestDto):
        data = await HttpGuestBot.request("/GetCrashWorks", dto)
        return data.get('Items')

    @staticmethod
    async def get_all_repairs(dto: GuestIdDto):
        data = await HttpGuestBot.request("/GetAllCrashWorks", dto)

        return data.get('Items')


class HttpChatBot(HttpClient):
    BASE_SERVICE = SERVER_BASE_SERVICE

    @staticmethod
    async def request(path: str, dto: AbstractDto):
        return await HttpClient.make_request(path, HttpChatBot.BASE_SERVICE, dto)

    @staticmethod
    async def fetch_streets(dto: SearchDto):
        data = await HttpChatBot.request("/SearchStreets", dto)
        return data.get("Streets")

    @staticmethod
    async def verify_address(dto: VerifyAddressDto):
        data = await HttpChatBot.request("/VerifyAddress", dto)
        return data.get("Correct")

    @staticmethod
    async def register(dto: RegisterDto):
        print(dto.to_payload())
        data = await HttpChatBot.request("/Register", dto)

        print(f'/Registter Data: {data}')
        return data.get("UserId")

    @staticmethod
    async def check_email(dto: CheckEmailDto):
        data = await HttpChatBot.request("/CheckEmail", dto)
        print(data)
        return data.get("Registration")

    @staticmethod
    async def code_to_email(dto: EmailDto):
        data = await HttpChatBot.request("/SendCode", dto)
        print(data)
        return data

    @staticmethod
    async def get_user_params(dto: UserIdDto):
        data = await HttpChatBot.request("/GetUserParams", dto)

        print(data)
        return data

    @staticmethod
    async def report_issue(dto: ReportIssueDto):
        return await HttpChatBot.request("/ReportIssue", dto)

    @staticmethod
    async def get_problems(dto: UserIdDto):
        data = await HttpChatBot.request("/GetProblems", dto)
        return data.get("Items")

    @staticmethod
    async def get_reasons(dto: ProblemIdDto):
        data = await HttpChatBot.request("/GetReasons", dto)
        return data.get("Items")

    @staticmethod
    async def get_address_by_geo(dto: AddressByGeoDto):
        return await HttpChatBot.request("/AddressByGeo", dto)

    @staticmethod
    async def create_request(dto: CreateRequestDto):
        print(dto.to_payload())
        data = await HttpChatBot.request("/CreateRequest", dto)

        print(data)
        return data.get("Id")

    @staticmethod
    async def actual_requests(dto: UserIdDto):
        data = await HttpChatBot.request("/ActualRequests", dto)
        return data.get("Requests")

    @staticmethod
    async def archived_requests(dto: UserIdDto):
        data = await HttpChatBot.request("/ArchivedRequests", dto)

        return data.get("Requests")

    @staticmethod
    async def get_enterprises(dto: UserIdDto):
        data = await HttpChatBot.request("/GetKps", dto)

        return data.get("Items")

    @staticmethod
    async def rate_enterprise(dto: RateEnterpriseDto):
        data = await HttpChatBot.request("/SaveKpRate", dto)

        return data.get("Status") == "ok"

    @staticmethod
    async def rate_request(dto: RateRequestDto):
        data = await HttpChatBot.request("/RateRequest", dto)

        return data.get("Status") == "ok"

    @staticmethod
    async def update_profile(dto: UpdateUserDto):
        data = await HttpChatBot.request("/UpdateUserParams", dto)

        return data.get("Status") == "ok"

    @staticmethod
    async def get_information(dto: ParentIdDto):
        data = await HttpChatBot.request("/GetInformations", dto)

        return data.get("Items")

    @staticmethod
    async def get_repairs(dto: RepairsDto):
        data = await HttpChatBot.request("/GetCrashWorks", dto)

        print(data)

        return data.get('Items')

    @staticmethod
    async def get_all_repairs(dto: RepairsDto):
        data = await HttpChatBot.request("/GetAllCrashWorks", dto)

        return data.get('Items')

    @staticmethod
    async def unique_phone(dto: PhoneDto):
        print(dto.to_payload())
        data = await HttpChatBot.request("/ValidateNumber", dto)
        print(data)

        return data.get('IsUniq')

    @staticmethod
    async def choise_region(dto: ChooseRegionDto):
        return await HttpGuestBot.request("/ChoiseRegion", dto)

    @staticmethod
    async def get_all_city(data) -> dict:
        response = await HttpInfoClient.post(
            data=data,
            full_url=f"{SERVER_BASE_URL}/Services/Dictionary/json/getcities",
        )

        return response.get("list")
