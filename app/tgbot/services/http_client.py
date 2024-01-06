import json
from typing import Sequence, TypeVar

import aiohttp

from data.config import SERVER_TOKEN, SERVER_BASE_URL, SERVER_BASE_SERVICE

T = TypeVar("T")


class HttpClient:
    basic_headers = {
        "Token": SERVER_TOKEN,
        "Content-Type": "application/json"
    }

    @staticmethod
    async def post(path: str, data: Sequence[T] | dict | None = None, service: str = None) -> dict:
        # TODO Try catch

        if data:
            data = json.dumps(data)

        async with aiohttp.ClientSession(headers=HttpClient.basic_headers) as session:
            if service:
                full_url = f"{SERVER_BASE_URL}/{service}{path}"
            else:
                full_url = f"{SERVER_BASE_URL}/{SERVER_BASE_SERVICE}{path}"

            print(full_url)

            async with session.post(url=full_url, data=data, ssl=False) as resp:
                return await resp.json()


async def fetch_streets(street: str) -> list:
    data = {"Search": street}

    response = await HttpClient.post('/SearchStreets', data)

    return response.get('Streets')


async def verify_address(street_id: int, house: str) -> bool:
    data = {
        "StreetId": street_id,
        "House": house
    }

    response = await HttpClient.post('/VerifyAddress', data)

    return response.get('Correct')


async def register(data: dict) -> bool:
    data = {
        "FirstName": data['FirstName'],
        "MiddleName": data['MiddleName'],
        "LastName": data['LastName'],
        "Gender": data['Phone'],
        "Phone": data['Password'],
        "CityId": data['StreetId'],
        "StreetId": data['House'],
        "House": data['House'],
        "Flat": data['Flat'],
        "Password": data['Password'],
        "Email": "data"
    }

    response = await HttpClient.post('/Register', data)

    return response.get('Correct')


async def check_email(email: str) -> bool:
    data = {
        "Email": email,
        "Platform": "telegram"
    }

    response = await HttpClient.post('/CheckEmail', data)

    print(response)

    return response.get('Registration')


async def send_code_to_email(email: str) -> dict:
    data = {
        "Email": email
    }

    response = await HttpClient.post('/SendCode', data)

    # TODO Remove this
    print(response)

    return response


async def get_user_params(user_id: int) -> dict:
    response = await HttpClient.post('/GetUserParams', {
        "UserId": user_id
    })

    # TODO Remove this
    print(response)

    return response


async def report_issue(data: dict):
    response = await HttpClient.post('/ReportIssue', data)

    # TODO Remove this
    print(response)

    return response


async def get_problems(user_id: int) -> list:
    response = await HttpClient.post('/GetProblems', {
        'UserId': user_id
    })

    # TODO Remove this
    print(response)

    return response.get('Items')


async def get_reasons(problem_id: int) -> list:
    response = await HttpClient.post('/GetReasons', {
        'ProblemId': problem_id
    })

    # TODO Remove this
    print(response)

    return response.get('Items')


async def get_address_by_geo(user_id: int, lat: float, lng: float):
    response = await HttpClient.post('/AddressByGeo', {
        "UserId": user_id,
        "Lat": lat,
        "Lng": lng
    })

    # TODO Remove this
    print(response)

    return response


async def create_request(data: dict) -> int:
    print(data)
    response = await HttpClient.post('/CreateRequest', data)

    # TODO Remove this
    print(response)
    #
    return response.get('Id')


async def get_street_by_id(street_id: int) -> dict:
    response = await HttpClient.post('/getstreetbyid', {
        "streetid": street_id
    }, 'Services/Dictionary/json')

    # TODO Remove this
    print(response)
    #
    return response.get('list')[0]


async def actual_requests(user_id: int) -> list:
    response = await HttpClient.post('/ActualRequests', {
        'UserId': user_id
    })

    # TODO Remove this
    print(response)
    #
    return response.get('Requests')


async def archived_requests(user_id: int) -> list:
    response = await HttpClient.post('/ArchivedRequests', {
        'UserId': user_id
    })

    # TODO Remove this
    print(response)
    #
    return response.get('Requests')


async def get_enterprises(user_id: int) -> list:
    response = await HttpClient.post('/GetKps', {
        'UserId': user_id
    })

    # TODO Remove this
    print(response)
    #
    return response.get('Items')


async def rate_enterprise(data: dict) -> bool:
    response = await HttpClient.post('/SaveKpRate', data)

    # TODO Remove this
    print(response)
    #
    return response.get('Status') == 'ok'


async def rate_request(data: dict) -> bool:
    response = await HttpClient.post('/RateRequest', data)

    # TODO Remove this
    print(response)
    #
    return response.get('Status') == 'ok'


async def update_profile(data: dict) -> bool:
    response = await HttpClient.post('/UpdateUserParams', data)

    # TODO Remove this
    print(response)
    #
    return response.get('Status') == 'ok'
