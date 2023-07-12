from typing import Any
import allure
from sqlalchemy import MetaData, Table, create_engine, select, func
from sqlalchemy.orm import sessionmaker
from models.users import UserInfo, User, UserDB
from models.cars import CarDB, Car
from models.house import HouseDB
from settings import settings


class Database:
    SCHEMA = 'public'

    def _connect(self):
        self.engine = create_engine(settings.sqlalchemy_database_uri.unicode_string())
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)
        session = sessionmaker(bind=self.engine)
        self.session = session()
        self.person_table = self.metadata.tables['person']
        self.car_table = self.metadata.tables['car']
        self.engine_type_table = self.metadata.tables['engine_type']
        self.house_table = self.metadata.tables['house']

    def close(self):
        self.session.close()

    @allure.step('Getting all users from DB')
    def get_users(self):
        stmt = select(self.person_table)
        data = self.session.execute(stmt).mappings().all()
        return data

    @allure.step(f'Getting user from DB by id == {id}')
    def get_user_by_id(self, id: int) -> UserDB:
        stmt = select(self.person_table).where(self.person_table.columns.id == id)
        data = self.session.execute(stmt).mappings().one()
        return UserDB(**data)

    @allure.step('Getting all cars from DB')
    def get_cars(self):
        stmt = select(self.car_table)
        data = self.session.execute(stmt).mappings().all()
        return data

    @allure.step(f'Getting car from DB by id == {id}')
    def get_car_by_id(self, id: int) -> CarDB:
        stmt = select(self.car_table).where(self.car_table.columns.id == id)
        data = self.session.execute(stmt).mappings().one()
        return CarDB(**data)

    def _filter(self, table: Table, where_params: dict[str, Any]):
        clauses = []
        for param in where_params:
            if param not in self.person_table.columns:
                raise ValueError(f'{param} нет в таблице person')
            clauses.append(self.person_table.columns.get(param) == where_params[param])
        stmt = select(table).where(*clauses)
        result = self.session.execute(stmt).mappings().all()
        return result

    @allure.step('Make select persons with params: {where_params}')
    def filter_users(self, where_params: dict[str, Any]):
        result = self._filter(self.person_table, where_params)
        return result

    @allure.step('Make select cars with params: {where_params}')
    def filter_cars(self, where_params: dict[str, Any]):
        result = self._filter(self.car_table, where_params)
        return result

    @allure.step('Make procedure name: {procedure_name}')
    def make_procedure(self, procedure_name, *args):
        try:
            connection = self.engine.raw_connection()
            cursor = connection.cursor()
            cursor.callproc(procedure_name, args)
            results = list(cursor.fetchall())
            cursor.close()
            connection.commit()
        finally:
            connection.close()
        return results

    @allure.step('Getting a random user with more than 2 cars')
    def get_random_user_more_2_cars(self) -> UserInfo:
        stmt = (
            select(self.person_table)
            .join(self.car_table)
            .group_by(self.person_table.c.id)
            .having(func.count(self.car_table.c.id) > 2)
        )
        user = self.session.execute(stmt).first()._mapping
        if not user:
            raise AssertionError('Не удалось найти пользователя для теста')
        user = UserInfo(
            **user,
            cars=[]
        )
        stmt = (
            select(self.car_table, self.engine_type_table.c.type_name.label('engineType'))
            .join(self.engine_type_table)
            .where(self.car_table.c.person_id == user.id)
        )
        cars = self.session.execute(stmt).mappings().all()
        user.cars = sorted([Car(**car) for car in cars], key=lambda x: x.id)
        return user

    @allure.step('Getting a random user')
    def get_random_user(self) -> UserDB:
        stmt = select(self.person_table).order_by(func.random()).limit(1)
        user = self.session.execute(stmt).mappings().one()
        return UserDB(**user)

    @allure.step('Getting a random car')
    def get_random_car_without_owner(self) -> CarDB:
        stmt = (
            select(self.car_table)
            .where(self.car_table.c.person_id.is_(None))
            .order_by(func.random())
            .limit(1)
        )
        car = self.session.execute(stmt).mappings().one()
        return CarDB(**car)

    @allure.step('Getting a user with money >= {need_money}')
    def get_user_with_right_amount_money(self, need_money: int) -> UserDB:
        stmt = (
            select(self.person_table)
            .where(self.person_table.c.money >= need_money)
            .order_by(func.random())
            .limit(1)
        )
        user = self.session.execute(stmt).mappings().one()
        return UserDB(**user)

    @allure.step('Getting a random house')
    def get_random_house(self) -> HouseDB:
        stmt = select(self.house_table).order_by(func.random()).limit(1)
        house = self.session.execute(stmt).mappings().one()
        return HouseDB(**house)

    @allure.step('Getting a user without house and money >= {need_money}')
    def get_user_with_right_amount_money_and_house(self, need_money: int) -> User:
        stmt = (
            select(self.person_table)
            .where(self.person_table.c.money >= need_money,
                   self.person_table.c.house_id.is_(None))
            .order_by(func.random())
            .limit(1)
        )
        user = self.session.execute(stmt).mappings().one()
        return User(**user)
