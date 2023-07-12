import allure
import pytest

from pages.login_page import LoginPage


@allure.feature('Авторизация')
class TestLoginPage:
    @allure.title('Проверка возможности авторизации с корректным логином и паролем')
    @pytest.mark.auth
    def test_can_login_with_correct_email_and_password(
        self,
        login_page: LoginPage
    ):
        login_page.email_input.fill('admin@pflb.ru')
        login_page.password_input.fill('admin')
        with login_page.page.expect_event('dialog') as dialog_info:
            login_page.page.once('dialog', lambda dialog: dialog.dismiss())
            login_page.authorize_button.click()
        dialog = dialog_info.value
        assert dialog.message == 'Successful authorization'

    @allure.title('Проверка невозможности авторизации с корректным логином и пустым паролем')
    @pytest.mark.xfail
    def test_cant_login_with_correct_email_and_empty_password(
        self,
        login_page: LoginPage
    ):
        login_page.email_input.fill('admin@pflb.ru')
        login_page.password_input.fill('admin')
        with login_page.page.expect_event('dialog') as dialog_info:
            login_page.page.once("dialog", lambda dialog: dialog.dismiss())
            login_page.authorize_button.click()
            dialog = dialog_info.value
            assert dialog.message == 'Incorrect input data'
