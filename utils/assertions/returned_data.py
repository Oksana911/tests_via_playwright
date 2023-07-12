from typing import Any
import allure


@allure.step('Check returned data == payload')
def check_returned_data(response_data: dict[str, Any], payload: dict[str, Any]):
    msg = 'Данные полученные в ответе API не совпадают с переданными'
    __assertion_data(response_data, payload, msg)


@allure.step('Check returned data == data in db')
def check_data_in_db(response_data: dict[str, Any], db_data: dict[str, Any]):
    msg = 'Данные полученные из БД не совпадают с ответом API'
    __assertion_data(response_data, db_data, msg)


def __assertion_data(response_data: dict[str, Any], data: dict[str, Any], msg: str):
    for key, value in data.items():
        if key in response_data:
            assert value == data[key], msg
