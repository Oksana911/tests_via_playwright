from http import HTTPStatus
from typing import Any

import allure
import jsonschema
import pytest

from api.base import Client
from api.user_api import create_user
from database.db import Database
from models.users import User
from utils.assertions.returned_data import (
    check_data_in_db,
    check_returned_data,
)
from utils.builders.user import UserBuilder


@allure.feature('Users')
@allure.story('Users API')
class TestUsers:
    @allure.title('Создание сущности user c валидными данными')
    @pytest.mark.parametrize(
        'payload',
        (
            UserBuilder().set_first_name('Василий').build(),
            UserBuilder().set_second_name('Рубенштейн').build(),
            UserBuilder().set_age(42).build(),
            UserBuilder().set_age(0).build(),
            UserBuilder().set_sex('MALE').build(),
            UserBuilder().set_sex('FEMALE').build(),
            UserBuilder().set_money(10000.01).build(),
            UserBuilder().set_money(-10000.01).build(),
            UserBuilder().set_money(0).build(),
        ),
    )
    def test_create_user(
        self, admin_auth_client: Client, db: Database, payload: dict[str, Any]
    ):
        response = create_user(admin_auth_client, payload)
        assert response.status == HTTPStatus.CREATED, 'Ошибка создания User'
        jsonschema.validate(response.json(), schema=User.schema())
        response_data = response.json()
        check_returned_data(response_data, payload)
        assert response_data.get('id') is not None, 'id не был сгенерирован'
        db_data = db.get_user_by_id(response_data.get('id'))
        check_data_in_db(response_data, db_data)

    @allure.title('Создаем сущность user с внесением id в запрос')
    def test_create_user_with_id(self, admin_auth_client: Client, db: Database):
        payload = UserBuilder().set_id(99).build()
        response = create_user(admin_auth_client, payload)
        assert response.status == HTTPStatus.CREATED, 'Ошибка создания User'
        jsonschema.validate(response.json(), schema=User.schema())
        response_data = response.json()
        check_returned_data(response_data, payload)
        assert response_data.get('id') is not None, 'id не был сгенерирован'
        db_data = db.get_user_by_id(response_data.get('id'))
        check_data_in_db(response_data, db_data)
        assert payload['id'] != response_data['id']

    @allure.title('Создание сущности user c невалидными данными')
    @pytest.mark.parametrize(
        'payload',
        (
            UserBuilder().set_first_name(None).build(),
            UserBuilder().set_first_name(1).build(),
            UserBuilder().set_first_name(1.2).build(),
            UserBuilder().set_first_name(False).build(),
            UserBuilder().set_second_name(None).build(),
            UserBuilder().set_second_name(1).build(),
            UserBuilder().set_second_name(1.2).build(),
            UserBuilder().set_second_name(False).build(),
            UserBuilder().set_age(-1).build(),
            UserBuilder().set_sex(0).build(),
            UserBuilder().set_sex(None).build(),
            UserBuilder().set_sex('NOTBINARY').build(),
            UserBuilder().set_age('forty').build(),
            UserBuilder().set_age(40.1).build(),
            UserBuilder().set_age(False).build(),
            UserBuilder().set_age(None).build(),
            UserBuilder().set_sex(1).build(),
            UserBuilder().set_sex(0.1).build(),
            UserBuilder().set_sex(False).build(),
            UserBuilder().set_money(None).build(),
            UserBuilder().set_money('money').build(),
            UserBuilder().set_money(False).build(),
        ),
    )
    def test_create_user_with_wrong_data(
        self, admin_auth_client: Client, db: Database, payload: dict[str, Any]
    ):
        response = create_user(admin_auth_client, payload)
        assert response.status == HTTPStatus.BAD_REQUEST, 'Ожидалось получение 400'
