import pytest
import allure
from http import HTTPStatus

from api.auth_api import auth_get, auth_post
from api.base import Client
from api.car_api import create_car, get_car, get_car_list, update_car, delete_car
from api.house_api import (
    create_house,
    get_house,
    get_house_list,
    delete_house,
    update_house,
    house_settle_user,
    house_evict_user,
)
from api.user_api import (
    get_user,
    get_user_list,
    update_user,
    create_user,
    delete_user,
    get_user_info,
    user_buy_car,
    user_add_money,
    user_sell_car,
)
from settings import settings


@allure.story('Authorization Test')
class TestAuthorization:
    @pytest.mark.parametrize(
            'payload',
            ({
                'username': settings.admin.username,
                'password': settings.admin.password,
             },
             {
                'username': settings.user.username,
                'password': settings.user.password,
             }),
            ids=('admin', 'user')
    )
    @pytest.mark.parametrize(
            'headers',
            ({'Content-Type': 'application/json'},
             {'Content-Type': 'application/json; charset=UTF-8'}),
            ids=('NoCharset', 'Charset')
    )
    @allure.title('login POST body')
    def test_authorization_post_body(self, client: Client, headers, payload):
        response = auth_post(client, payload, headers=headers)
        assert response.status == HTTPStatus.ACCEPTED
        data = response.json()
        assert 'access_token' in data
        headers['Authorization'] = f'Bearer {data["access_token"]}'
        response = get_user(client, 1, headers=headers)
        assert response.status == HTTPStatus.OK

    @pytest.mark.parametrize(
            'params',
            ({
                'username': settings.admin.username,
                'password': settings.admin.password,
             },
             {
                'username': settings.user.username,
                'password': settings.user.password,
             }),
            ids=('admin', 'user')
    )
    @pytest.mark.parametrize(
            'headers',
            ({'Content-Type': 'application/x-www-form-urlencoded'},
             {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}),
            ids=('NoCharset', 'Charset')
    )
    @allure.title('login POST url')
    def test_authorization_post_url(self, client: Client, headers, params):
        response = auth_post(client, headers=headers, params=params)
        assert response.status == HTTPStatus.ACCEPTED
        data = response.json()
        assert 'access_token' in data
        headers['Authorization'] = f'Bearer {data["access_token"]}'
        response = get_user(client, 1, headers=headers)
        assert response.status == HTTPStatus.OK

    @allure.title('login GET method')
    @pytest.mark.parametrize(
            'params',
            ({
                'username': settings.admin.username,
                'password': settings.admin.password,
             },
             {
                'username': settings.user.username,
                'password': settings.user.password,
             }),
            ids=('admin', 'user')
    )
    @pytest.mark.parametrize(
            'headers',
            ({'Content-Type': r'application/x-www-form-urlencoded'},
             {'Content-Type': r'application/x-www-form-urlencoded; charset=UTF-8'}),
            ids=('NoCharset', 'Charset')
    )
    def test_authorization_get_method(self, client: Client, params, headers):
        response = auth_get(client, params=params, headers=headers)
        assert response.status == HTTPStatus.ACCEPTED
        data = response.json()
        assert 'access_token' in data
        headers['Authorization'] = f'Bearer {data["access_token"]}'
        response = get_user(client, 1, headers=headers)
        assert response.status == HTTPStatus.OK


@allure.story('Car Test')
class TestCar:

    @allure.title('Test Car')
    def test_car(self, admin_auth_client, car_payload, new_car_payload):
        response_json = self.__admin_add_car(admin_auth_client, car_payload)
        self.__admin_check_add_car(admin_auth_client, response_json)
        self.__admin_check_add_car_list(admin_auth_client, response_json)
        self.__admin_update_car(admin_auth_client, response_json['id'], new_car_payload)
        self.__admin_check_update_car(
            admin_auth_client, response_json['id'], new_car_payload
        )
        self.__admin_delete_car(admin_auth_client, response_json['id'])
        self.__admin_check_delete_car(admin_auth_client, response_json['id'])

    @allure.step('ADMIN AddCar')
    def __admin_add_car(self, admin_auth_client, car_payload) -> dict:
        response = create_car(admin_auth_client, payload=car_payload)
        assert response.status == HTTPStatus.CREATED
        return response.json()

    @allure.step('ADMIN CheckAddCar')
    def __admin_check_add_car(self, admin_auth_client, car_json):
        response = get_car(admin_auth_client, car_json.get('id'))
        assert response.status == HTTPStatus.OK
        assert car_json == response.json()

    @allure.step('ADMIN CheckAddCarList')
    def __admin_check_add_car_list(self, admin_auth_client, car_json):
        response = get_car_list(admin_auth_client)
        assert response.status == HTTPStatus.OK
        car_list = response.json()
        assert car_json in car_list

    @allure.step('ADMIN UpdateCar')
    def __admin_update_car(self, admin_auth_client, car_id, car_json):
        response = update_car(admin_auth_client, car_id, car_json)
        assert response.status == HTTPStatus.ACCEPTED

    @allure.step('ADMIN CheckUpdateCar')
    def __admin_check_update_car(self, admin_auth_client, car_id, new_car_data):
        response = get_car(admin_auth_client, car_id)
        assert response.status == HTTPStatus.OK
        new_car_data['id'] = car_id
        assert new_car_data == response.json()

    @allure.step('ADMIN DeleteCar')
    def __admin_delete_car(self, admin_auth_client, car_id):
        response = delete_car(admin_auth_client, car_id)
        assert response.status == HTTPStatus.NO_CONTENT

    @allure.step('ADMIN CheckDeleteCar')
    def __admin_check_delete_car(self, admin_auth_client, car_id):
        response = get_car(admin_auth_client, car_id)
        assert response.status == HTTPStatus.NO_CONTENT


@allure.story('House Test')
class TestHouse:

    @allure.title('Test House')
    def test_house(self, admin_auth_client, house_payload, new_house_payload):
        response_json = self.__admin_add_house(admin_auth_client, house_payload)
        self.__admin_check_add_house(admin_auth_client, response_json)
        self.__admin_check_add_house_list(admin_auth_client, response_json)
        new_house_data = self.__admin_update_house(
            admin_auth_client, response_json['id'], new_house_payload
        )
        self.__admin_check_update_house(
            admin_auth_client, response_json['id'], new_house_data
        )
        self.__admin_delete_house(admin_auth_client, response_json['id'])
        self.__admin_check_delete_house(admin_auth_client, response_json['id'])

    @allure.step('ADMIN AddHouse')
    def __admin_add_house(self, admin_auth_client, house_payload) -> dict:
        response = create_house(admin_auth_client, payload=house_payload)
        assert response.status == HTTPStatus.CREATED
        return response.json()

    @allure.step('ADMIN CheckAddHouse')
    def __admin_check_add_house(self, admin_auth_client, house_json):
        response = get_house(admin_auth_client, house_json.get('id'))
        assert response.status == HTTPStatus.OK
        assert house_json == response.json()

    @allure.step('ADMIN CheckAddHouseList')
    def __admin_check_add_house_list(self, admin_auth_client, house_json):
        response = get_house_list(admin_auth_client)
        assert response.status == HTTPStatus.OK
        house_list = response.json()
        assert house_json in house_list

    @allure.step('ADMIN UpdateHouse')
    def __admin_update_house(self, admin_auth_client, house_id, house_json):
        response = update_house(admin_auth_client, house_id, house_json)
        assert response.status == HTTPStatus.ACCEPTED
        return response.json()

    @allure.step('ADMIN CheckUpdateHouse')
    def __admin_check_update_house(self, admin_auth_client, house_id, new_house_data):
        response = get_house(admin_auth_client, house_id)
        assert response.status == HTTPStatus.OK
        assert new_house_data == response.json()

    @allure.step('ADMIN DeleteHouse')
    def __admin_delete_house(self, admin_auth_client, house_id):
        response = delete_house(admin_auth_client, house_id)
        assert response.status == HTTPStatus.NO_CONTENT

    @allure.step('ADMIN CheckDeleteHouse')
    def __admin_check_delete_house(self, admin_auth_client, house_id):
        response = get_house(admin_auth_client, house_id)
        assert response.status == HTTPStatus.NO_CONTENT


@allure.story('User Test')
class TestUser:

    @allure.title('Test User')
    def test_user(self, admin_auth_client, user_payload, new_user_payload):
        response_json = self.__admin_add_user(admin_auth_client, user_payload)
        self.__admin_check_add_user(admin_auth_client, response_json)
        self.__admin_check_add_user_list(admin_auth_client, response_json)
        new_user_data = self.__admin_update_user(
            admin_auth_client, response_json['id'], new_user_payload
        )
        self.__admin_check_update_user(
            admin_auth_client, response_json['id'], new_user_data
        )
        self.__admin_delete_user(admin_auth_client, response_json['id'])
        self.__admin_check_delete_user(admin_auth_client, response_json['id'])

    @allure.step('ADMIN AddUser')
    def __admin_add_user(self, admin_auth_client, user_payload) -> dict:
        response = create_user(admin_auth_client, payload=user_payload)
        assert response.status == HTTPStatus.CREATED
        return response.json()

    @allure.step('ADMIN CheckAddUser')
    def __admin_check_add_user(self, admin_auth_client, user_json):
        response = get_user(admin_auth_client, user_json.get('id'))
        assert response.status == HTTPStatus.OK
        assert user_json == response.json()

    @allure.step('ADMIN CheckAddUserList')
    def __admin_check_add_user_list(self, admin_auth_client, user_json):
        response = get_user_list(admin_auth_client)
        assert response.status == HTTPStatus.OK
        user_list = response.json()
        assert user_json in user_list

    @allure.step('ADMIN UpdateUser')
    def __admin_update_user(self, admin_auth_client, user_id, user_json):
        response = update_user(admin_auth_client, user_id, user_json)
        assert response.status == HTTPStatus.ACCEPTED
        return response.json()

    @allure.step('ADMIN CheckUpdateUser')
    def __admin_check_update_user(self, admin_auth_client, user_id, new_user_data):
        response = get_user(admin_auth_client, user_id)
        assert response.status == HTTPStatus.OK
        assert new_user_data == response.json()

    @allure.step('ADMIN DeleteUser')
    def __admin_delete_user(self, admin_auth_client, user_id):
        response = delete_user(admin_auth_client, user_id)
        assert response.status == HTTPStatus.NO_CONTENT

    @allure.step('ADMIN CheckDeleteUser')
    def __admin_check_delete_user(self, admin_auth_client, user_id):
        response = get_user(admin_auth_client, user_id)
        assert response.status == HTTPStatus.NO_CONTENT


@allure.story('User Car Test')
class TestUserCar:
    def test_user_car(
        self,
        admin_auth_client,
        user_payload,
        car_payload,
        new_car_payload,
        new_user_payload,
    ):
        user_json = self.__admin_add_user(admin_auth_client, user_payload)
        self.__admin_check_users_cars(admin_auth_client, user_json)
        car_json = self.__admin_add_car(admin_auth_client, car_payload)
        self.__admin_check_add_car(admin_auth_client, car_json)
        #
        self.__admin_buy_car_not_money(admin_auth_client, user_json, car_json)
        self.__admin_add_users_money(admin_auth_client, user_json['id'])
        self.__admin_buy_car(admin_auth_client, user_json, car_json)
        self.__admin_check_buy_car(admin_auth_client, user_json, car_json)
        self.__admin_cant_delete_user(admin_auth_client, user_json)
        self.__admin_cant_delete_car(admin_auth_client, car_json)
        self.__admin_user_sell_car(admin_auth_client, user_json, car_json)
        self.__admin_check_sell_car(admin_auth_client, user_json, car_json)
        #
        self.__admin_buy_car(admin_auth_client, user_json, car_json)
        self.__admin_check_buy_car(admin_auth_client, user_json, car_json)
        self.__admin_cant_update_car(admin_auth_client, car_json['id'], new_car_payload)
        self.__admin_check_not_sell_on_update(admin_auth_client, user_json, car_json)
        self.__admin_user_sell_car(admin_auth_client, user_json, car_json)
        self.__admin_check_sell_car(admin_auth_client, user_json, car_json)
        #
        self.__admin_buy_car(admin_auth_client, user_json, car_json)
        self.__admin_check_buy_car(admin_auth_client, user_json, car_json)
        self.__admin_cant_update_user(admin_auth_client, user_json['id'], new_user_payload)
        self.__admin_check_not_sell_on_update(admin_auth_client, user_json, car_json)
        self.__admin_user_sell_car(admin_auth_client, user_json, car_json)
        self.__admin_check_sell_car(admin_auth_client, user_json, car_json)
        #
        self.__admin_delete_car(admin_auth_client, car_json)
        self.__admin_check_delete_car(admin_auth_client, car_json['id'])
        self.__admin_delete_user(admin_auth_client, user_json)
        self.__admin_check_delete_user(admin_auth_client, user_json['id'])

    @allure.step('ADMIN AddUser')
    def __admin_add_user(self, admin_auth_client, user_payload) -> dict:
        response = create_user(admin_auth_client, payload=user_payload)
        assert response.status == HTTPStatus.CREATED
        return response.json()

    @allure.step('ADMIN CheckUsersCars')
    def __admin_check_users_cars(self, admin_auth_client, user) -> dict:
        response = get_user_info(admin_auth_client, user['id'])
        assert response.status == HTTPStatus.OK
        user_data = response.json()
        cars = user_data.pop('cars')
        user_data.pop('house')
        assert len(cars) == 0
        assert user == user_data

    @allure.step('ADMIN AddCar')
    def __admin_add_car(self, admin_auth_client, car_payload) -> dict:
        response = create_car(admin_auth_client, payload=car_payload)
        assert response.status == HTTPStatus.CREATED
        return response.json()

    @allure.step('ADMIN CheckAddCar')
    def __admin_check_add_car(self, admin_auth_client, car_json):
        response = get_car(admin_auth_client, car_json.get('id'))
        assert response.status == HTTPStatus.OK
        assert car_json == response.json()

    @allure.step('ADMIN NotEnoughMoney')
    def __admin_buy_car_not_money(self, admin_auth_client, user_json, car_json):
        response = user_buy_car(admin_auth_client, user_json['id'], car_json['id'])
        assert response.status == HTTPStatus.NOT_ACCEPTABLE

    @allure.step('ADMIN UserAddMoney')
    def __admin_add_users_money(self, admin_auth_client, user_id):
        response = user_add_money(admin_auth_client, user_id, 1000000)
        assert response.status == HTTPStatus.OK

    @allure.step('ADMIN BuyCarForUser')
    def __admin_buy_car(self, admin_auth_client, user_json, car_json):
        response = user_buy_car(admin_auth_client, user_json['id'], car_json['id'])
        assert response.status == HTTPStatus.OK

    @allure.step('ADMIN CheckBuyCar')
    def __admin_check_buy_car(self, admin_auth_client, user_json, car_json):
        response = get_user_info(admin_auth_client, user_json['id'])
        assert response.status == HTTPStatus.OK
        new_user_info = response.json()
        cars = new_user_info.pop('cars')
        assert cars == [car_json]

    @allure.step('ADMIN CantDeleteUser')
    def __admin_cant_delete_user(self, admin_auth_client, user_json):
        response = delete_user(admin_auth_client, user_json['id'])
        assert response.status == HTTPStatus.CONFLICT

    @allure.step('ADMIN  CantDeleteCar')
    def __admin_cant_delete_car(self, admin_auth_client, car_json):
        response = delete_car(admin_auth_client, car_json['id'])
        assert response.status == HTTPStatus.CONFLICT

    @allure.step('ADMIN SellUsersCar')
    def __admin_user_sell_car(self, admin_auth_client, user_json, car_json):
        response = user_sell_car(admin_auth_client, user_json['id'], car_json['id'])
        assert response.status == HTTPStatus.OK

    @allure.step('ADMIN CheckSellCar')
    def __admin_check_sell_car(self, admin_auth_client, user_json, car_json):
        response = get_user_info(admin_auth_client, user_json['id'])
        assert response.status == HTTPStatus.OK
        new_user_info = response.json()
        cars = new_user_info.pop('cars')
        assert len(cars) == 0

    @allure.step('ADMIN  CantUpdateCar')
    def __admin_cant_update_car(self, admin_auth_client, car_id, new_car_payload):
        response = update_car(admin_auth_client, car_id, new_car_payload)
        assert response.status == HTTPStatus.CONFLICT

    @allure.step('ADMIN NotSelledOnUpdate')
    def __admin_check_not_sell_on_update(self, admin_auth_client, user_json, car_json):
        response = get_user_info(admin_auth_client, user_json['id'])
        assert response.status == HTTPStatus.OK
        new_user_info = response.json()
        cars = new_user_info.pop('cars')
        assert len(cars) != 0

    @allure.step('ADMIN CantUpdateUser')
    def __admin_cant_update_user(self, admin_auth_client, user_id, new_user_payload):
        response = update_user(admin_auth_client, user_id, new_user_payload)
        assert response.status == HTTPStatus.CONFLICT

    @allure.step('ADMIN DeleteCar')
    def __admin_delete_car(self, admin_auth_client, car_json):
        response = delete_car(admin_auth_client, car_json['id'])
        assert response.status == HTTPStatus.NO_CONTENT

    @allure.step('ADMIN DeleteUser')
    def __admin_delete_user(self, admin_auth_client, user_json):
        response = delete_user(admin_auth_client, user_json['id'])
        assert response.status == HTTPStatus.NO_CONTENT

    @allure.step('ADMIN CheckDeleteCar')
    def __admin_check_delete_car(self, admin_auth_client, car_id):
        response = get_car(admin_auth_client, car_id)
        assert response.status == HTTPStatus.NO_CONTENT

    @allure.step('ADMIN CheckDeleteUser')
    def __admin_check_delete_user(self, admin_auth_client, user_id):
        response = get_user(admin_auth_client, user_id)
        assert response.status == HTTPStatus.NO_CONTENT


@allure.story('House Lodgers Tests')
class TestHouseLodgers:
    def test_house_lodgers(
            self,
            user_auth_client: Client,
            house_payload,
            new_house_payload,
            user_payload,
            new_user_payload,
    ):
        house_json = self.__user_add_house(user_auth_client, house_payload)
        self.__user_check_add_house(user_auth_client, house_json)
        user_json = self.__user_add_user(user_auth_client, user_payload)
        self.__user_check_add_user(user_auth_client, user_json)
        #
        self.__user_settle_not_money(user_auth_client, user_json, house_json)
        self.__user_add_users_money(user_auth_client, user_json['id'])
        self.__user_settle_user(user_auth_client, user_json, house_json)
        self.__user_check_settle_user(user_auth_client, house_json['id'], user_json)
        self.__user_cant_delete_house(user_auth_client, house_json)
        self.__user_cant_delete_user(user_auth_client, user_json)
        self.__user_evict_user(user_auth_client, user_json, house_json)
        self.__user_check_evict_user(user_auth_client, house_json['id'])
        #
        self.__user_settle_user(user_auth_client, user_json, house_json)
        self.__user_check_settle_user(user_auth_client, house_json['id'], user_json)
        self.__user_cant_update_house(
            user_auth_client, house_json['id'], new_house_payload
        )
        self.__user_check_update_house(user_auth_client, house_json.copy())
        self.__user_evict_user(user_auth_client, user_json, house_json)
        self.__user_check_evict_user(user_auth_client, house_json['id'])
        #
        self.__user_settle_user(user_auth_client, user_json, house_json)
        self.__user_check_settle_user(user_auth_client, house_json['id'], user_json)
        self.__user_cant_update_user(user_auth_client, user_json['id'], new_user_payload)
        self.__user_check_update_house(user_auth_client, house_json.copy())
        self.__user_evict_user(user_auth_client, user_json, house_json)
        self.__user_check_evict_user(user_auth_client, house_json['id'])
        #
        self.__user_delete_user(user_auth_client, user_json['id'])
        self.__user_check_delete_user(user_auth_client, user_json['id'])
        self.__user_delete_house(user_auth_client, house_json['id'])
        self.__user_check_delete_house(user_auth_client, house_json['id'])

    @allure.step('USER AddHouse')
    def __user_add_house(self, user_auth_client, house_payload) -> dict:
        response = create_house(user_auth_client, payload=house_payload)
        assert response.status == HTTPStatus.CREATED
        return response.json()

    @allure.step('USER CheckAddHouse')
    def __user_check_add_house(self, user_auth_client, house_json):
        response = get_house(user_auth_client, house_json.get('id'))
        assert response.status == HTTPStatus.OK
        assert house_json == response.json()

    @allure.step('USER AddUser')
    def __user_add_user(self, user_auth_client, user_payload) -> dict:
        response = create_user(user_auth_client, payload=user_payload)
        assert response.status == HTTPStatus.CREATED
        return response.json()

    @allure.step('USER CheckAddUser')
    def __user_check_add_user(self, user_auth_client, user_json):
        response = get_user(user_auth_client, user_json.get('id'))
        assert response.status == HTTPStatus.OK
        assert user_json == response.json()

    @allure.step('USER NotEnoughMoney')
    def __user_settle_not_money(self, user_auth_client, user_json, house_json):
        response = house_settle_user(user_auth_client, house_json['id'], user_json['id'])
        assert response.status == HTTPStatus.NOT_ACCEPTABLE

    @allure.step('USER UserAddMoney')
    def __user_add_users_money(self, user_auth_client, user_id):
        response = user_add_money(user_auth_client, user_id, 1000000)
        assert response.status == HTTPStatus.OK

    @allure.step('USER SettleUser')
    def __user_settle_user(self, user_auth_client, user_json, house_json):
        response = house_settle_user(user_auth_client, house_json['id'], user_json['id'])
        assert response.status == HTTPStatus.OK

    @allure.step('USER CheckSettleUser')
    def __user_check_settle_user(self, user_auth_client, house_id, user_json):
        response = get_house(user_auth_client, house_id)
        assert response.status == HTTPStatus.OK
        assert user_json['id'] == response.json()['lodgers'][0]['id']

    @allure.step('USER  CantDeleteHouse')
    def __user_cant_delete_house(self, user_auth_client, house_json):
        response = delete_house(user_auth_client, house_json['id'])
        assert response.status == HTTPStatus.CONFLICT

    @allure.step('USER CantDeleteUser')
    def __user_cant_delete_user(self, user_auth_client, user_json):
        response = delete_user(user_auth_client, user_json['id'])
        assert response.status == HTTPStatus.CONFLICT

    @allure.step('USER EvictUser')
    def __user_evict_user(self, user_auth_client, user_json, house_json):
        response = house_evict_user(user_auth_client, house_json['id'], user_json['id'])
        assert response.status == HTTPStatus.OK

    @allure.step('USER CheckEvictUser')
    def __user_check_evict_user(self, user_auth_client, house_id):
        response = get_house(user_auth_client, house_id)
        assert response.status == HTTPStatus.OK
        assert len(response.json()['lodgers']) == 0

    @allure.step('USER  CantUpdateHouse')
    def __user_cant_update_house(self, user_auth_client, house_id, new_house_payload):
        response = update_house(user_auth_client, house_id, new_house_payload)
        assert response.status == HTTPStatus.CONFLICT

    @allure.step('USER NotEvictedOnUpdate')
    def __user_check_update_house(self, user_auth_client, house_json):
        response = get_house(user_auth_client, house_json['id'])
        assert response.status == HTTPStatus.OK
        new_house_data = response.json()
        house_json.pop('lodgers')
        lodgers = new_house_data.pop('lodgers')
        assert house_json == new_house_data
        assert len(lodgers) != 0

    @allure.step('USER CantUpdateUser')
    def __user_cant_update_user(self, user_auth_client, user_id, new_user_payload):
        response = update_user(user_auth_client, user_id, new_user_payload)
        assert response.status == HTTPStatus.CONFLICT

    @allure.step('USER DeleteUser')
    def __user_delete_user(self, user_auth_client, user_id):
        response = delete_user(user_auth_client, user_id)
        assert response.status == HTTPStatus.NO_CONTENT

    @allure.step('USER CheckDeleteUser')
    def __user_check_delete_user(self, user_auth_client, user_id):
        response = get_user(user_auth_client, user_id)
        assert response.status == HTTPStatus.NO_CONTENT

    @allure.step('USER DeleteHouse')
    def __user_delete_house(self, user_auth_client, house_id):
        response = delete_house(user_auth_client, house_id)
        assert response.status == HTTPStatus.NO_CONTENT

    @allure.step('USER CheckDeleteHouse')
    def __user_check_delete_house(self, user_auth_client, house_id):
        response = get_house(user_auth_client, house_id)
        assert response.status == HTTPStatus.NO_CONTENT


@allure.story('House Parking Place Tests')
class TestHouseParkingPlace:
    def test_house_parking_place(
        self,
        admin_auth_client,
        house_payload,
        house_without_parking,
        replace_house_payload,
    ):
        house_json = self.__admin_add_house(admin_auth_client, house_payload)
        self.__admin_check_add_house(admin_auth_client, house_json)
        house_json = self.__admin_delete_parking(
            admin_auth_client, house_json['id'], house_without_parking
        )
        self.__admin_check_update_house(admin_auth_client, house_json['id'], house_json)
        house_json = self.__admin_add_parking(
            admin_auth_client, house_json['id'], house_payload
        )
        self.__admin_check_update_house(admin_auth_client, house_json['id'], house_json)
        house_json = self.__admin_replace_house(
            admin_auth_client, house_json['id'], replace_house_payload
        )
        self.__admin_check_update_house(admin_auth_client, house_json['id'], house_json)

    @allure.step('ADMIN AddHouse')
    def __admin_add_house(self, admin_auth_client, house_payload) -> dict:
        response = create_house(admin_auth_client, payload=house_payload)
        assert response.status == HTTPStatus.CREATED
        return response.json()

    @allure.step('ADMIN CheckAddHouse')
    def __admin_check_add_house(self, admin_auth_client, house_json):
        response = get_house(admin_auth_client, house_json.get('id'))
        assert response.status == HTTPStatus.OK
        assert house_json == response.json()

    @allure.step('ADMIN DeleteParkingByPut')
    def __admin_delete_parking(self, admin_auth_client, house_id, payload):
        response = update_house(admin_auth_client, house_id, payload)
        assert response.status == HTTPStatus.ACCEPTED
        return response.json()

    @allure.step('ADMIN CheckUpdateHouse')
    def __admin_check_update_house(self, admin_auth_client, house_id, new_house_data):
        response = get_house(admin_auth_client, house_id)
        assert response.status == HTTPStatus.OK
        assert new_house_data == response.json()

    @allure.step('ADMIN AddParkingByPut')
    def __admin_add_parking(self, admin_auth_client, house_id, payload):
        response = update_house(admin_auth_client, house_id, payload)
        assert response.status == HTTPStatus.ACCEPTED
        return response.json()

    @allure.step('ADMIN ReplaceHouse')
    def __admin_replace_house(self, admin_auth_client, house_id, payload):
        response = update_house(admin_auth_client, house_id, payload)
        assert response.status == HTTPStatus.ACCEPTED
        return response.json()
