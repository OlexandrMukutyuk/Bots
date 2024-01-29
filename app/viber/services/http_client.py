import json

import aiofiles
import aiohttp

from data.config import SERVER_TOKEN, SERVER_BASE_URL, SERVER_BASE_SERVICE, SERVER_GUEST_SERVICE
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
    RateEnterpriseDto,
    ParentIdDto,
)
from dto.chat_bot.register import RegisterDto
from dto.chat_bot.repairs import RepairsDto
from dto.guest import UpdateGuestDto, GuestIdDto, RegisterGuestDto, RateEnterpriseGuestDto
from dto.guest.repairs_guest import RepairsGuestDto


class HttpClient:
    basic_headers = {"Token": SERVER_TOKEN, "Content-Type": "application/json"}

    @staticmethod
    async def make_request(path: str, service: str, dto: AbstractDto):
        res = await HttpClient.post(data=dto.to_payload(), path=path, service=service)

        # print(f"{path}: {res}")

        return res

    @staticmethod
    async def post(data: dict, **kwargs) -> dict:
        encoded_data = json.dumps(data)

        full_url: str = kwargs.get("full_url")

        async with aiohttp.ClientSession(headers=HttpClient.basic_headers) as session:
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
        print(dto.to_payload())
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
        return data.get("Items")

    @staticmethod
    async def get_all_repairs(dto: GuestIdDto):
        data = await HttpGuestBot.request("/GetAllCrashWorks", dto)

        return data.get("Items")


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
        return data.get("Correct")

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
        return await HttpChatBot.request("/GetUserParams", dto)

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
        data = await HttpChatBot.request("/CreateRequest", dto)

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

        return data.get("Items")


async def download_image(url, path):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                async with aiofiles.open(path, mode="wb") as f:
                    await f.write(await resp.read())


# Usage
# asyncio.run(download_image('http://example.com/image.jpg', '/path/to/save/image.jpg'))
