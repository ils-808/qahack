import pytest
import allure
from models.game_models import UserBase, Users
import faker

f = faker.Faker()


@allure.feature("User API")
@allure.story("User creation")
@pytest.mark.parametrize("x_task_value", ["api-3"])
def test_create_user_nick_used(api_client, x_task_value):
    dto = UserBase(email=f.email(), nickname=f.user_name(), password=f.password(), name=f.name())
    dto.model_dump(exclude_none=True)
    response = api_client.create_user(dto, x_task_value)

    assert UserBase(**response.json()).nickname, f"Empty nickname"


@allure.feature("User API")
@allure.story("User list")
@pytest.mark.parametrize("x_task_value", ["api-21"])
def test_total_users(api_client, x_task_value):
    response = api_client.get_users(x_task_value, 0)

    dto = Users(**response.json())

    assert dto.meta.total >= len(
        dto.users), f"Total amount of user: {dto.meta.total} less than amount of users in list {len(dto.users)}"


@allure.feature("User API")
@allure.story("User list offset")
@pytest.mark.parametrize("offset, x_task_value", [(5, "api-6")])
def test_total_users_amount(api_client, x_task_value, offset):
    response = api_client.get_users(x_task_value, offset)

    dto = Users(**response.json())

    assert len(
        dto.users) == min(10,
                          dto.meta.total - offset), f"Expected {dto.meta.total - offset} to show. Displayed {len(dto.users)}"


@allure.feature("User API")
@allure.story("Delete user")
@pytest.mark.parametrize("x_task_value", ["api-1"])
def test_delete_nonexisting_user(api_client, x_task_value):
    response = api_client.delete_user(f.uuid4(), x_task_value)

    assert response.status_code == 404, f"Incorrect response code: {response.status_code}"


@allure.feature("User API")
@allure.story("Update user partially")
@pytest.mark.parametrize("x_task_value", ["api-4"])
def test_update_user_email_already_exist(api_client, x_task_value):
    users_response = api_client.get_users(x_task_value, 0)
    users = Users(**users_response.json())

    dto = UserBase(email=users.users[0].email, nickname=users.users[0].nickname, password=f.password(), name=f.name())
    dto.model_dump(exclude_none=True)
    response = api_client.patch_user(dto, users.users[1].uuid, x_task_value)

    assert response.status_code == 409, f"Incorrect response code: {response.status_code}"


@allure.feature("User API")
@allure.story("Authenticate user")
@pytest.mark.parametrize("email, pwd, x_task_value",
                         [("d4@l.66d", "\"HA\"R\"HA\"R", "api-7")])
def test_login(api_client, email, pwd, x_task_value):
    dto = UserBase(email=email, password=pwd, name=f.name(), nickname=f.user_name())
    dto.model_dump(exclude_none=True)
    api_client.create_user(dto, x_task_value)
    response = api_client.auth_user(dto, x_task_value)

    assert response.status_code == 200, f"Authentication failed with code: {response.status_code}"


@allure.feature("User API")
@allure.story("Create user")
@pytest.mark.parametrize("x_task_value", ["api-22"])
def test_user_create(api_client, x_task_value):
    dto = UserBase(email=f.email(), password=f.password(), name=f.name(), nickname=f.user_name())
    dto.model_dump(exclude_none=True)
    response = api_client.create_user(dto, x_task_value)

    assert response.status_code == 200, f"Create user failed with code: {response.status_code}"


@allure.feature("User API")
@allure.story("Get user")
@pytest.mark.parametrize("x_task_value", ["api-23"])
def test_get_single_user(api_client, x_task_value):
    users_response = api_client.get_users(x_task_value, 0)
    users = Users(**users_response.json())
    user_uuid = users.users[len(users.users) - 1].uuid

    user_response = api_client.get_user(user_uuid, x_task_value)
    user = UserBase(**user_response.json())

    assert user.uuid == user_uuid, f"User ID mismatch: {user.uuid}"


@allure.feature("User API")
@allure.story("Update user password")
@pytest.mark.parametrize("x_task_value", ["api-24"])
def test_update_userpwd_and_login(api_client, x_task_value):
    users_response = api_client.get_users(x_task_value, 0)
    users = Users(**users_response.json())

    new_pass = f.password()
    dto = UserBase(email=users.users[0].email, password=new_pass, name=f.name(), nickname=users.users[0].nickname)
    dto.model_dump(exclude_none=True)
    api_client.patch_user(dto, users.users[0].uuid, x_task_value)

    response = api_client.auth_user(dto, x_task_value)

    assert response.status_code == 200, f"Unable login with new credentials, status code: {response.status_code}"
