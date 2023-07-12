import random

import allure
import pytest

from pages.add_money_page import PlusMoneyPage
from database.db import Database


@allure.feature('Plus Money Page')
class TestPlusMoneyPage:

    @allure.title('Тест добавления денег пользователю')
    @pytest.mark.auth
    def test_add_money(
        self,
        plus_money_page: PlusMoneyPage,
        db: Database
    ):
        user_before = db.get_random_user()
        # заполняем поля и выполняем запрос
        money = random.randint(100, 1000)
        plus_money_page.money_input.fill(str(money), True)
        plus_money_page.user_id_input.fill(str(user_before.id), True)
        plus_money_page.push_button.click()
        plus_money_page.page.wait_for_load_state('networkidle')
        # выполняем проверки UI
        plus_money_page.request_status_button.should_have_text(
            'Status: Successfully pushed, code: 200'
        )
        plus_money_page.new_user_money_button.should_be_visible()
        new_money = user_before.money + money
        displayed_money = str(int(new_money)) if int(new_money) == new_money else str(new_money)
        plus_money_page.new_user_money_button.should_have_text(displayed_money)
        # проверяем что данные в БД обновились
        user_after = db.get_user_by_id(user_before.id)
        assert user_before.money + money == user_after.money, \
               'Не обновилась информация о счете юзера'
