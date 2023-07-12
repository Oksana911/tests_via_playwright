import allure
from playwright.sync_api import Response

from api.base import Client


@allure.step('Getting access_token GET method')
def auth_get(client: Client, params: dict[str, str], **kwargs) -> Response:
    url = '/login'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    headers = headers if 'headers' not in kwargs else kwargs.pop('headers')
    return client.get(url, params=params, headers=headers, **kwargs)


@allure.step('Getting access_token POST method')
def auth_post(client: Client, payload: dict[str, str] = {}, **kwargs) -> Response:
    url = '/login'
    return client.post(url, json=payload, **kwargs)
