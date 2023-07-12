from typing import Any

import allure
from playwright.sync_api import Response

from api.base import Client


@allure.step('Creating Car')
def create_car(client: Client, payload: dict[str, Any]) -> Response:
    url = '/car/'
    return client.post(url, json=payload)


@allure.step('Getting Car')
def get_car(client: Client, id: int) -> Response:
    url = f'/car/{id}'
    return client.get(url)


@allure.step('Getting Cars list')
def get_car_list(client: Client) -> Response:
    url = '/cars'
    return client.get(url)


@allure.step('Updating Car')
def update_car(client: Client, id: int, payload: dict[str, Any]) -> Response:
    url = f'/car/{id}'
    return client.put(url, json=payload)


@allure.step('Deleting Car')
def delete_car(client: Client, id: int) -> Response:
    url = f'/car/{id}'
    return client.delete(url)
