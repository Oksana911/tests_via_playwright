from playwright.sync_api import Page
from pages.base_page import BasePage
from components.page_factory.button import Button
from components.page_factory.table import Table


class AllUsersPage(BasePage):
    URL = 'http://77.50.236.203:4881/#/read/users'

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.reload_button = Button(
            page=page,
            locator='//button[contains(@class,"btn btn-primary")]',
            name='reload button'
        )
        self.users_table = Table(
            page=page,
            locator='//table[contains(@class, "table table-striped table-bordered table-hover")]',
            name='users table'
        )
