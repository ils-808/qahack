import pytest
import allure

from models.game_models import UserBase, Users
import faker

from utils import prepare_file

f = faker.Faker()


@allure.feature("User API")
@allure.story("Update user avatar")
@pytest.mark.parametrize("x_task_value", ["api-11"])
#@pytest.mark.skip("doesn't work in github currently")
def test_update_avatar(api_client, x_task_value):
    users_response = api_client.get_users(x_task_value, 0)
    users = Users(**users_response.json())

    dto = UserBase(email=users.users[0].email, name=f.name(), nickname=users.users[0].nickname)
    dto.model_dump(exclude_none=True)

    file_name = 'ava.jpeg'
    file_content = prepare_file(file_name)
    update_response = api_client.upload_avatar(users.users[0].uuid, file_name, file_content, x_task_value)

    updated_user = UserBase(**update_response.json())
    response = api_client.check_file_availability(updated_user.avatar_url)
    assert response.status_code == 200, "File wasn't saved"
#
# def test_file_preparation():
#     try:
#         file_name = 'ava.jpg'
#         file_content = prepare_file(file_name)
#         pass
#     except Exception as e:
#         pytest.exit(f"Failed to prepare file: {e}")
