import allure

from database.db import Database
from models.users import User


@allure.feature('Procedure')
@allure.story('Procedure DB')
class TestProcedure:
    @allure.title('Тестируем процедуру "rename_users_by_first_name_and_second_name"')
    def test_procedure(self, db: Database, new_5_users: list[User], new_user: User):
        procedure_name = 'rename_users_by_first_name_and_second_name'
        new_name = 'NewNameTest'
        new_second_name = 'NewSecondNameTest'
        db.make_procedure(
            procedure_name,
            new_5_users[0].firstName,
            new_5_users[0].secondName,
            new_name,
            new_second_name,
        )
        persons_after = db.filter_users(
            where_params={
                'first_name': new_name,
                'second_name': new_second_name,
            },
        )
        ids_before = {person.id for person in new_5_users}
        ids_after = {person['id'] for person in persons_after}
        assert all(
            id in ids_after for id in ids_before
        ), 'firstName и secondName поменялся не у всех'
        assert (
            new_user.id not in ids_after
        ), 'firstName и secondName поменялся у лишнего пользователя'
