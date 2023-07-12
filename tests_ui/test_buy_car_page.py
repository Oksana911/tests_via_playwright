import allure
import pytest

from pages.buy_car_page import BuyCarPage
from database.db import Database


@allure.feature('Buy Car Page')
class TestBuyCarPage:

    @allure.title('Тест покупки машины пользователем')
    @pytest.mark.auth
    def test_buy_car(
        self,
        buy_car_page: BuyCarPage,
        db: Database
    ):
        car_before = db.get_random_car_without_owner()
        user_before = db.get_user_with_right_amount_money(car_before.price)

        buy_car_page.user_id_input.fill(str(user_before.id))
        buy_car_page.car_id_input.fill(str(car_before.id))
        buy_car_page.buy_radio_button.check(validate_value=True)
        buy_car_page.push_button.click()
        buy_car_page.page.wait_for_load_state('networkidle')

        buy_car_page.request_status_button.should_have_text(
            'Status: Successfully pushed, code: 200'
        )

        car_after = db.get_car_by_id(car_before.id)
        assert car_after.person_id == user_before.id, 'Не изменилась запись машины в БД'
        user_after = db.get_user_by_id(user_before.id)
        assert user_before.money - car_before.price == user_after.money, \
               'Неправильное кол-во денег после покупки'
