import allure
from playwright.sync_api import Page, Response
from components.constructions.header import Header
# from components.navigation.navbar import Navbar


class BasePage:
    URL: str

    def __init__(self, page: Page) -> None:
        self.page = page
        self.header = Header(page)
        self.url = self.URL

    def visit(self) -> Response | None:
        with allure.step(f'Opening the url "{self.url}"'):
            return self.page.goto(self.url, wait_until='networkidle')

    def reload(self) -> Response | None:
        with allure.step(f'Reloading page with url "{self.page.url}"'):
            return self.page.reload(wait_until='domcontentloaded')

