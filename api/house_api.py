from typing import Any

import allure
from playwright.sync_api import Response

from api.base import Client


@allure.step('Creating House')
def create_house(client: Client, payload: dict[str, Any]) -> Response:
    url = '/house/'
    return client.post(url, json=payload)


@allure.step('Getting House')
def get_house(client: Client, id: int) -> Response:
    url = f'/house/{id}'
    return client.get(url)


@allure.step('Getting Houses list')
def get_house_list(client: Client) -> Response:
    url = '/houses'
    return client.get(url)


@allure.step('Updating House')
def update_house(client: Client, id: int, payload: dict[str, Any]) -> Response:
    url = f'/house/{id}'
    return client.put(url, json=payload)


@allure.step('Deleting House')
def delete_house(client: Client, id: int) -> Response:
    url = f'/house/{id}'
    return client.delete(url)


@allure.step('Settle House')
def house_settle_user(client: Client, house_id: int, user_id: int) -> Response:
    url = f'/house/{house_id}/settle/{user_id}'
    return client.post(url)


@allure.step('Evict House')
def house_evict_user(client: Client, house_id: int, user_id: int) -> Response:
    url = f'/house/{house_id}/evict/{user_id}'
    return client.post(url)
