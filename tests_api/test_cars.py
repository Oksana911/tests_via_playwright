from http import HTTPStatus
from typing import Any

import allure
import jsonschema
import pytest

from api.base import Client
from api.car_api import create_car
from database.db import Database
from models.cars import Car
from utils.assertions.returned_data import (
    check_data_in_db,
    check_returned_data,
)
from utils.builders.car import CarBuilder


@allure.feature('Cars')
@allure.story('Cars API')
class TestCars:
    @allure.title('Создание сущности car c валидными данными')
    @pytest.mark.parametrize(
        'payload',
        (
            CarBuilder().set_engine_type('Gasoline').build(),
            CarBuilder().set_engine_type('PHEV').build(),
            CarBuilder().set_engine_type('Hydrogenic').build(),
            CarBuilder().set_engine_type('Electric').build(),
            CarBuilder().set_engine_type('Diesel').build(),
            CarBuilder().set_engine_type('CNG').build(),
            CarBuilder().set_mark('Тесла').build(),
            CarBuilder().set_model('Модель Икс').build(),
            CarBuilder().set_price(80000.00).build(),
            CarBuilder().set_id(666).build(),
        ),
    )
    def test_create_car(self, admin_auth_client: Client, db: Database, payload: dict[str, Any]):
        response = create_car(admin_auth_client, payload)
        assert response.status == HTTPStatus.CREATED, 'Ошибка создания Car'
        jsonschema.validate(response.json(), schema=Car.schema())
        response_data = response.json()
        check_returned_data(response_data, payload)
        assert response_data.get('id') is not None, 'id не был сгенерирован'
        check_data_in_db(response_data, response_data)

    @allure.title('Создание сущности car, у которой Id внесен в запрос,')
    def test_create_car_with_id(self, admin_auth_client: Client, db: Database):
        payload = CarBuilder().set_id(666).build()
        response = create_car(admin_auth_client, payload)
        assert response.status == HTTPStatus.CREATED, 'Ошибка создания Car'
        jsonschema.validate(response.json(), schema=Car.schema())
        response_data = response.json()
        check_returned_data(response_data, payload)
        assert response_data.get('id') is not None, 'id не был сгенерирован'
        check_data_in_db(response_data, response_data)
        assert payload['id'] != response_data['id']

    @allure.title('Создание сущности car c валидными данными')
    @pytest.mark.parametrize(
        'payload',
        (
            CarBuilder().set_engine_type(None).build(),
            CarBuilder().set_engine_type('Coal').build(),
            CarBuilder().set_engine_type(1).build(),
            CarBuilder().set_engine_type(0.1).build(),
            CarBuilder().set_engine_type(False).build(),
            CarBuilder().set_mark(None).build(),
            CarBuilder().set_mark(1).build(),
            CarBuilder().set_mark(0.1).build(),
            CarBuilder().set_mark(False).build(),
            CarBuilder().set_model(None).build(),
            CarBuilder().set_model(1).build(),
            CarBuilder().set_model(0.1).build(),
            CarBuilder().set_model(False).build(),
            CarBuilder().set_price(None).build(),
            CarBuilder().set_price(-10000).build(),
            CarBuilder().set_price('money').build(),
            CarBuilder().set_price(False).build(),
        ),
    )
    def test_create_car_with_wrong_data(
        self, admin_auth_client: Client, db: Database, payload: dict[str, Any]
    ):
        count_cars = len(db.get_cars())
        response = create_car(admin_auth_client, payload)
        assert response.status == HTTPStatus.BAD_REQUEST, 'Ожидалось получение 400'
        count_cars_after = len(db.get_cars())
        assert (
            count_cars == count_cars_after
        ), 'Машина не должна была создаться, но создалась'
