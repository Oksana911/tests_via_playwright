from playwright.sync_api import Page

from components.page_factory.button import Button
from components.page_factory.input import Input
from components.page_factory.table import Table
from pages.base_page import BasePage


class UserInfoPage(BasePage):
    URL = 'http://77.50.236.203:4881/#/read/userInfo'

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.id_input = Input(
            page,
            locator='//input[@id="user_input"]',
            name='user id input',
        )
        self.search_button = Button(
            page,
            locator='//button[contains(@class,"btn-primary")]',
            name='search button'
        )
        self.cars_table = Table(
            page,
            locator='//table[contains(@class, "tableCars")]',
            name='cars table',
        )
        self.user_table = Table(
            page,
            locator='//table[contains(@class, "tableUser")]',
            name='user table',
        )
