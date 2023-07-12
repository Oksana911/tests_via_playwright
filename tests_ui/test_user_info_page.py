import time

import allure
import pytest

from pages.user_info_page import UserInfoPage
from database.db import Database
from utils.html_table_to_json import HtmlTableParser
from models.users import UserInfo
from models.cars import Car


@allure.feature('User Info Page')
class TestUserInfoPage:

    @allure.title('Проверка ответа формы')
    @pytest.mark.auth
    def test_response_object_mapping_db_object(
        self,
        user_info_page: UserInfoPage,
        db: Database
    ):
        user_db = db.get_random_user_more_2_cars()
        user_info_page.id_input.fill(str(user_db.id), validate_value=True)
        user_info_page.search_button.click()
        time.sleep(2)  # TODO подумать над нормальным ожиданием

        # получаем HTML код таблиц и парсим в JSON
        html = user_info_page.cars_table.get_inner_html()
        table_cars = HtmlTableParser(html).get_json()
        html = user_info_page.user_table.get_inner_html()
        table_user = HtmlTableParser(html).get_json()
        assert len(table_user) == 1, 'На странице должна быть информация об 1 человеке'

        # проверяем соответствие полученного объекта объектам в базе
        table_user = table_user[0]
        table_user.pop('cars')
        user = UserInfo(
            **table_user,
            cars=sorted([Car(**car) for car in table_cars], key=lambda x: x.id),
        )
        assert user.dict() == user_db.dict(), 'Данные в бд и UI не совпадают'
