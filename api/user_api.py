from typing import Any

import allure
from playwright.sync_api import Response

from api.base import Client


@allure.step('Creating User')
def create_user(client: Client, payload: dict[str, Any]) -> Response:
    url = '/user/'
    return client.post(url, json=payload)


@allure.step('Deleting User')
def delete_user(client: Client, id: int) -> Response:
    url = f'/user/{id}'
    return client.delete(url)


@allure.step('Getting User ID: {id}')
def get_user(client: Client, id: int, **kwargs) -> Response:
    url = f'/user/{id}'
    return client.get(url, **kwargs)


@allure.step('Getting User list')
def get_user_list(client: Client, **kwargs) -> Response:
    url = '/users'
    return client.get(url, **kwargs)


@allure.step('Updating User')
def update_user(client: Client, id: int, payload: dict[str, Any]) -> Response:
    url = f'/user/{id}'
    return client.put(url, json=payload)


@allure.step('Getting User Info')
def get_user_info(client: Client, id: int) -> Response:
    url = f'/user/{id}/info'
    return client.get(url)


@allure.step('User ID: {user_id} buy Car ID: {car_id}')
def user_buy_car(
    client: Client,
    user_id: int,
    car_id: int,
) -> Response:
    url = f'/user/{user_id}/buyCar/{car_id}'
    return client.post(url)


@allure.step('User ID: {user_id} sell Car ID: {car_id}')
def user_sell_car(
    client: Client,
    user_id: int,
    car_id: int,
) -> Response:
    url = f'/user/{user_id}/sellCar/{car_id}'
    return client.post(url)


@allure.step('Add many {money} to User ID: {user_id}')
def user_add_money(client: Client, user_id: int, money: int) -> Response:
    url = f'/user/{user_id}/money/{money}'
    return client.post(url)
