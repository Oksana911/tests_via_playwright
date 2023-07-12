from playwright.sync_api import Page

from components.page_factory.button import Button
from components.page_factory.input import Input, RadioInput
from pages.base_page import BasePage


class BuyCarPage(BasePage):
    URL = 'http://77.50.236.203:4881/#/update/users/buyCar'

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.user_id_input = Input(
            page=page,
            locator='//input[@id="id_send"]',
            name='user id input'
        )
        self.car_id_input = Input(
            page=page,
            locator='//input[@id="car_send"]',
            name='car id input'
        )
        self.buy_radio_button = RadioInput(
            page=page,
            locator='//input[@type="radio" and @value="buyCar"]',
            name='buy radio button',
        )
        self.sell_radio_button = RadioInput(
            page=page,
            locator='//input[@type="radio" and @value="sellCar"]',
            name='sell radio button',
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
