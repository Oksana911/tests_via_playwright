import random

import allure
import pytest

from pages.create_user_page import CreateUserPage
from database.db import Database


@allure.feature('Create User Page')
class TestCreateUserPage:

    @allure.title('Тест страницы создания пользователя')
    @pytest.mark.auth
    def test_create_user(
        self,
        create_user_page: CreateUserPage,
        db: Database
    ):
        user_data = {
            'first_name': 'Vasiliy',
            'second_name': 'Rubenstein',
            'age': 42,
            'sex': 'MALE',
            'money': random.randint(44444, 555555),
        }
        create_user_page.first_name_input.fill(user_data['first_name'])
        create_user_page.last_name_input.fill(user_data['second_name'])
        create_user_page.money_input.fill(str(user_data['money']))
        create_user_page.age_input.fill(str(user_data['age']))
        create_user_page.sex_male_radio_button.check(validate_value=True)
        create_user_page.push_button.click()
        create_user_page.page.wait_for_load_state('networkidle')

        create_user_page.request_status_button.should_have_text(
            'Status: Successfully pushed, code: 201'
        )
        where_param = user_data.copy()
        where_param.pop('sex')
        users = db.filter_users(where_param)
        if len(users) != 1:
            raise ValueError('Не получилось отфильтровать созданного юзера')
        user = users[0]

        create_user_page.new_id_button.should_have_text(f'New user ID: {user.get("id")}')
