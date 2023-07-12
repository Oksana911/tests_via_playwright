import pytest


@pytest.fixture()
def car_payload():
    return {
        'engineType': 'Electric',
        'mark': 'postman',
        'model': 'e2e_test',
        'price': 10000.00
    }


@pytest.fixture()
def new_car_payload():
    return {
        'engineType': 'PHEV',
        'mark': 'e2e_test',
        'model': 'postman',
        'price': 0.00
    }


@pytest.fixture()
def house_payload():
    return {
        'floorCount': 2,
        'price': 10001.00,
        'parkingPlaces': [
            {
                'id': 1,
                'isWarm': False,
                'isCovered': True,
                'placesCount': 3
            }
        ]
    }


@pytest.fixture()
def new_house_payload():
    return {
        'floorCount': 3,
        'price': 3939.00,
        'parkingPlaces': [
            {
                'id': 1,
                'isWarm': True,
                'isCovered': False,
                'placesCount': 33
            }
        ]
    }


@pytest.fixture()
def house_without_parking():
    return {
        'floorCount': 9,
        'price': 9393.00,
        'parkingPlaces': []
    }


@pytest.fixture()
def replace_house_payload():
    return {
        'floorCount': 3,
        'price': 3939.00,
        'parkingPlaces': [
            {
                'isWarm': True,
                'isCovered': True,
                'placesCount': 39
            }
        ]
    }


@pytest.fixture()
def user_payload():
    return {
        'firstName': 'postman',
        'secondName': 'test',
        'age': 42,
        'sex': 'MALE',
        'money': 0.00
    }


@pytest.fixture()
def new_user_payload():
    return {
        'firstName': 'e2e_test',
        'secondName': 'postman',
        'age': 24,
        'sex': 'FEMALE',
        'money': 0.00
    }
