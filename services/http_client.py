import json
from typing import Sequence, TypeVar

import aiohttp

from data.config import SERVER_TOKEN, SERVER_BASE_URL

T = TypeVar("T")


class HttpClient:
    basic_headers = {
        "Token": SERVER_TOKEN,
        "Content-Type": "application/json"
    }

    @staticmethod
    async def post(path: str, data: Sequence[T] | dict | None = None) -> dict:
        # TODO Try catch

        if data:
            data = json.dumps(data)

        async with aiohttp.ClientSession(headers=HttpClient.basic_headers) as session:
            full_url = f"{SERVER_BASE_URL}{path}"

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

    return response.get('Registration')


async def send_code_to_email(email: str) -> dict:
    data = {
        "Email": email
    }

    response = await HttpClient.post('/SendCode', data)

    return response
