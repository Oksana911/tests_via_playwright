from playwright.sync_api import Page

from components.page_factory.button import Button
from components.page_factory.input import Input
from pages.base_page import BasePage


class PlusMoneyPage(BasePage):
    URL = 'http://77.50.236.203:4881/#/update/users/plusMoney'

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.user_id_input = Input(
            page=self.page,
            locator='//input[@id="id_send"]',
            name='user id input'
        )

        self.money_input = Input(
            page=self.page,
            locator='//input[@id="money_send"]',
            name='money input'
        )

        self.push_button = Button(
            page=self.page,
            locator='//button[contains(@class,"btn-primary")]',
            name='push to API button'
        )

        self.request_status_button = Button(
            page=self.page,
            locator='//button[contains(@class,"status btn btn-secondary")]',
            name='status button'
        )

        self.new_user_money_button = Button(
            page=self.page,
            locator='//button[contains(@class,"money btn btn-secondary")]',
            name='user money button'
        )
