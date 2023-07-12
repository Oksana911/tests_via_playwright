from datetime import datetime
import allure
import pytest
import requests
from http import HTTPStatus
from allure_commons.types import AttachmentType
from playwright.sync_api import Page, sync_playwright, Playwright
from pathlib import Path
from settings import settings
from database.db import Database
from pages.user_info_page import UserInfoPage
from pages.login_page import LoginPage
from pages.add_money_page import PlusMoneyPage
from pages.buy_car_page import BuyCarPage
from pages.house_and_user_page import HouseUserPage
from pages.create_user_page import CreateUserPage
from pages.all_users_page import AllUsersPage
from api.base import Client
from api.user_api import create_user, delete_user
from models.users import User
from utils.builders.user import UserBuilder


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для создания скриншотов падающих тестов"""
    outcome = yield
    rep = outcome.get_result()
    if rep.when == 'call' and rep.failed:
        if 'browser' in item.fixturenames:
            browser = item.funcargs['browser']
            file_name = f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}" \
                .replace("/", "_").replace("::", "__")
            screen_path = Path().absolute() / 'allure-results' / f'error_{file_name}.png'
            browser.save_screenshot(screen_path)
            allure.attach.file(
                source=screen_path,
                name=f'error {file_name}',
                attachment_type=AttachmentType.PNG
            )


@pytest.fixture(scope='session')
def token():
    payload = {
        'username': settings.user.username,
        'password': settings.user.password,
    }
    login_url = 'http://77.50.236.203:4879/login'   #  TODO
    response = requests.post(login_url, data=payload)
    assert response.status_code == HTTPStatus.ACCEPTED, 'Ошибка получения токена.'
    token = response.json().get('access_token')
    assert token is not None
    return token


@pytest.fixture(scope='function')
def chromium_page(token, request) -> Page:
    with sync_playwright() as playwright:
        auth = request.node.get_closest_marker('auth')
        chromium = playwright.chromium.launch(headless=False)
        if auth:
            auth_header = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            context = chromium.new_context(extra_http_headers=auth_header)
            context.add_cookies(
                [{
                    'name': 'jwt',
                    'value': token,
                    'url': 'http://77.50.236.203:4881/'
                }]
            )
            page = context.new_page()
        else:
            page = chromium.new_page()
        yield page


@pytest.fixture(scope='function')
def login_page(chromium_page: Page) -> LoginPage:
    page = LoginPage(chromium_page)
    page.visit()
    return page


@pytest.fixture(scope='function')
def user_info_page(chromium_page: Page) -> UserInfoPage:
    page = UserInfoPage(chromium_page)
    page.visit()
    return page


@pytest.fixture(scope='function')
def buy_car_page(chromium_page: Page) -> BuyCarPage:
    page = BuyCarPage(chromium_page)
    page.visit()
    return page


@pytest.fixture(scope='function')
def plus_money_page(chromium_page: Page) -> PlusMoneyPage:
    page = PlusMoneyPage(chromium_page)
    page.visit()
    return page


@pytest.fixture(scope='function')
def house_and_user_page(chromium_page: Page) -> HouseUserPage:
    page = HouseUserPage(chromium_page)
    page.visit()
    return page


@pytest.fixture(scope='function')
def create_user_page(chromium_page: Page) -> CreateUserPage:
    page = CreateUserPage(chromium_page)
    page.visit()
    return page


@pytest.fixture(scope='function')
def all_users_page(chromium_page: Page) -> AllUsersPage:
    page = AllUsersPage(chromium_page)
    page.visit()
    return page


@pytest.fixture(scope='session')
def admin_auth_client(playwright: Playwright):
    client = Client.get_client(playwright, authenticate=True, admin=True)
    yield client
    client.close()


@pytest.fixture(scope='session')
def user_auth_client(playwright: Playwright):
    client = Client.get_client(playwright, authenticate=True, admin=False)
    yield client
    client.close()


@pytest.fixture(scope='session')
def client(playwright: Playwright):
    client = Client.get_client(playwright)
    yield client
    client.close()


@pytest.fixture(scope='function')
def new_user(admin_auth_client: Client):
    response = create_user(admin_auth_client, UserBuilder().set_first_name('Test').build())
    user = User(**response.json())
    yield user
    delete_user(admin_auth_client, user.id)


@pytest.fixture(scope='function')
def new_5_users(admin_auth_client: Client):
    users = [
        User(**create_user(admin_auth_client, UserBuilder().build()).json()) for _ in range(5)
    ]
    yield users
    for user in users:
        delete_user(admin_auth_client, user.id)


@pytest.fixture(scope='session')
def db():
    db = Database()
    db._connect()
    yield db
    db.close()
