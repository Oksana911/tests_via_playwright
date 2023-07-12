from playwright.sync_api import Page
from components.page_factory.button import Button
from components.page_factory.input import Input, RadioInput
from pages.base_page import BasePage


class HouseUserPage(BasePage):
    URL = 'http://77.50.236.203:4881/#/update/houseAndUser'

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.user_id_input = Input(
            page=self.page,
            locator='//input[@id="id_send"]',
            name='user id input'
        )
        self.house_id_input = Input(
            page=self.page,
            locator='//input[@id="house_send"]',
            name='house id input'
        )
        self.settle_radio_button = RadioInput(
            page=page,
            locator='//input[@type="radio" and @value="settle"]',
            name='settle radio button',
        )
        self.evict_radio_button = RadioInput(
            page=page,
            locator='//input[@type="radio" and @value="evict"]',
            name='evict radio button',
        )
        self.request_status_button = Button(
            page=self.page,
            locator='//button[contains(@class,"status btn btn-secondary")]',
            name='status button'
        )
        self.push_button = Button(
            page=self.page,
            locator='//button[contains(@class,"btn-primary")]',
            name='push to API button'
        )
