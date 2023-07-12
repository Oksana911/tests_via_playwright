import allure
import pytest


from pages.house_and_user_page import HouseUserPage
from database.db import Database


@allure.feature('House User Page')
class TestHouseUserPage:

    @allure.title('Тест заселение пользователя')
    @pytest.mark.auth
    def test_user_settle_in_house(
        self,
        house_and_user_page: HouseUserPage,
        db: Database
    ):
        house = db.get_random_house()
        user_before = db.get_user_with_right_amount_money_and_house(house.price)

        house_and_user_page.user_id_input.fill(str(user_before.id))
        house_and_user_page.house_id_input.fill(str(house.id))
        house_and_user_page.settle_radio_button.check(validate_value=True)
        house_and_user_page.push_button.click()
        house_and_user_page.page.wait_for_load_state('networkidle')

        house_and_user_page.request_status_button.should_have_text(
            'Status: Successfully pushed, code: 200'
        )

        user_after = db.get_user_by_id(user_before.id)
        assert user_after.house_id == house.id, 'Неверный id Дома у пользователя в БД'
        assert user_before.money - house.price == user_after.money, \
               'Неверное кол-во денег у пользователя'
