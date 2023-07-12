from playwright.sync_api import Page
from pages.base_page import BasePage
from components.page_factory.button import Button
from components.page_factory.input import Input


class LoginPage(BasePage):
    URL = 'http://77.50.236.203:4881/'

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.email_input = Input(
            page,
            locator='//input[@name="email"]',
            name='email input'
        )
        self.password_input = Input(
            page,
            locator='//input[@name="password"]',
            name='password input'
        )
        self.authorize_button = Button(
            page,
            locator='//button[contains(@class,"btn-primary")]',
            name='authorize button'
        )
