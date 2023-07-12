from playwright.sync_api import Page


class Header:
    def __init__(self, page: Page) -> None:
        self.page = page
