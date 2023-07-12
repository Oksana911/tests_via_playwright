import allure
from playwright.sync_api import expect
from components.page_factory.component import Component


class Input(Component):
    @property
    def type_of(self) -> str:
        return 'input'

    def fill(self, value: str, validate_value=False, **kwargs):
        with allure.step(f'Fill {self.type_of} "{self.name}" to value "{value}"'):
            locator = self.get_locator(**kwargs)
            locator.fill(value)

            if validate_value:
                self.should_have_value(value, **kwargs)

    def should_have_value(self, value: str, **kwargs):
        with allure.step(f'Checking that {self.type_of} "{self.name}" has a value "{value}"'):
            locator = self.get_locator(**kwargs)
            expect(locator).to_have_value(value)


class RadioInput(Component):
    @property
    def type_of(self) -> str:
        return 'radio button'

    def check(self, validate_value=False):
        with allure.step(f'Choice {self.type_of} "{self.name}"'):
            locator = self.get_locator()
            locator.check()

        if validate_value:
            assert locator.is_checked() is True, 'Radio кнопка не выбралась'
