from decimal import Decimal

import allure
from pages.all_users_page import AllUsersPage
from database.db import Database
from utils.html_table_to_json import HtmlTableParser
from models.users import User


@allure.feature('All user Page')
class TestAllUserPage:
    @allure.title('Тест получения всех пользователей')
    def test_get_all_user(
        self,
        all_users_page: AllUsersPage,
        db: Database
    ):
        assert all_users_page.page.title() == 'PFLB Test-API', 'Неверный Title'
        html = all_users_page.users_table.get_inner_html()
        table_data = HtmlTableParser(html).get_json()

        ui_users = [
            User(**user) for user in sorted(table_data, key=lambda x: int(x.get('id')))
        ]

        db_users = db.get_users()
        db_users = [
            User(**user) for user in sorted(db_users, key=lambda x: x.get('id'))
        ]

        assert ui_users == db_users, 'Неверно отображены пользователи'
