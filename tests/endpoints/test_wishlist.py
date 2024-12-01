import pytest
import allure
from models.game_models import GamesResponse, Users, GameWishlist


@allure.feature("Wishlist API")
@allure.story("Add item to wishlist")
@pytest.mark.parametrize("x_task_value", ["api-5"])
def test_add_item_wishlist(api_client, x_task_value):
    games = api_client.get_games(x_task_value)
    games_dto = GamesResponse(**games.json())
    users_response = api_client.get_users(x_task_value, 0)
    users_dto = Users(**users_response.json())

    user_uuid = users_dto.users[0].uuid
    gamed_uuid = games_dto.games[0].uuid

    response = api_client.add_item_whishlist(user_uuid, gamed_uuid, x_task_value)

    assert response.status_code == 200, f"Add item to wishlist failed with code: {response.status_code}"


@allure.feature("Wishlist API")
@allure.story("Remove item from wishlist")
@pytest.mark.parametrize("x_task_value", ["api-8"])
def test_remove_item_wishlist(api_client, x_task_value):
    users_response = api_client.get_users(x_task_value, 0)
    users_dto = Users(**users_response.json())

    games = api_client.get_games(x_task_value)
    games_dto = GamesResponse(**games.json())

    user_uuid = users_dto.users[0].uuid
    gamed_uuid = games_dto.games[0].uuid

    api_client.add_item_whishlist(user_uuid, gamed_uuid, x_task_value)
    wishlist_response = api_client.get_whishlist(user_uuid, x_task_value)
    wishlist_dto = GameWishlist(**wishlist_response.json())

    item_uuid_delete = wishlist_dto.items[0].uuid
    delete_response = api_client.delete_item_whishlist(user_uuid, item_uuid_delete, x_task_value)
    updated_wishlist_dto = GameWishlist(**delete_response.json())

    assert item_uuid_delete not in [item.uuid for item in
                                    updated_wishlist_dto.items], f"Item wash delete from wishlist: {item_uuid_delete}"


@allure.feature("Wishlist API")
@allure.story("Duplicate item in wishlist")
@pytest.mark.parametrize("x_task_value", ["api-25"])
def test_add_duplicate_item_wishlist(api_client, x_task_value):
    users_response = api_client.get_users(x_task_value, 0)
    users_dto = Users(**users_response.json())

    user_uuid = users_dto.users[0].uuid

    wishlist_response = api_client.get_whishlist(user_uuid, x_task_value)
    wishlist_dto = GameWishlist(**wishlist_response.json())
    item_to_add = wishlist_dto.items[0].uuid

    response = api_client.add_item_whishlist(user_uuid, item_to_add, x_task_value)
    updated_wishlist_dto = GameWishlist(**response.json())

    all_uuids = [item.uuid for item in updated_wishlist_dto.items]

    # Проверяем, что длина списка UUID равна длине множества UUID
    assert len(all_uuids) == len(set(all_uuids)), "Duplicate items in wishlist"
