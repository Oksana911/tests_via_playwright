from playwright.sync_api import Page

from components.page_factory.button import Button
from components.page_factory.input import Input, RadioInput
from pages.base_page import BasePage


class CreateUserPage(BasePage):
    URL = 'http://77.50.236.203:4881/#/create/user'

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.first_name_input = Input(
            page=page,
            locator='//input[@id="first_name_send"]',
            name='first name input',
        )
        self.last_name_input = Input(
            page=page,
            locator='//input[@id="last_name_send"]',
            name='last name input',
        )
        self.age_input = Input(
            page=page,
            locator='//input[@id="age_send"]',
            name='age input',
        )
        self.age_input = Input(
            page=page,
            locator='//input[@id="age_send"]',
            name='age input',
        )
        self.sex_male_radio_button = RadioInput(
            page=page,
            locator='//input[@type="radio" and @value="MALE"]',
            name='sex male radio button',
        )
        self.sex_female_radio_button = RadioInput(
            page=page,
            locator='//input[@type="radio" and @value="FEMALE"]',
            name='sex female radio button',
        )
        self.money_input = Input(
            page=page,
            locator='//input[@id="money_send"]',
            name='money input',
        )
        self.request_status_button = Button(
            page=page,
            locator='//button[contains(@class,"status btn btn-secondary")]',
            name='status button',
        )
        self.new_id_button = Button(
            page=page,
            locator='//button[contains(@class,"newId btn btn-secondary")]',
            name='new user id button',
        )
        self.push_button = Button(
            page=page,
            locator='//button[contains(@class,"btn-primary")]',
            name='push to API button',
        )
