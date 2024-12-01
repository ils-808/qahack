import pytest
import allure
from models.game_models import GamesResponse, Users, Cart, CartResponse


@allure.feature("Cart API")
@allure.story("Get cart")
@pytest.mark.parametrize("x_task_value", ["api-12"])
def test_get_cart(api_client, x_task_value):
    games = api_client.get_games(x_task_value)
    games_dto = GamesResponse(**games.json())
    users_response = api_client.get_users(x_task_value, 0)
    users_dto = Users(**users_response.json())

    user_uuid = users_dto.users[0].uuid
    gamed_uuid = games_dto.games[0].uuid

    new_cart_item = Cart(item_uuid=gamed_uuid, quantity=1)

    api_client.add_to_cart(user_uuid, new_cart_item, x_task_value)

    response = api_client.get_cart(user_uuid, x_task_value)
    order_dto = CartResponse(**response.json())
    total_amount_array = sum(item.total_price for item in order_dto.items)
    assert total_amount_array == order_dto.total_price, f"Amount in array doens't equal total amount: {order_dto.total_price}"


@allure.feature("Cart API")
@allure.story("Remove an item from cart")
@pytest.mark.parametrize("x_task_value", ["api-14"])
def test_delete_item(api_client, x_task_value):
    games = api_client.get_games(x_task_value)
    games_dto = GamesResponse(**games.json())
    users_response = api_client.get_users(x_task_value, 0)
    users_dto = Users(**users_response.json())

    user_uuid = users_dto.users[0].uuid

    first_cart_item = Cart(item_uuid=games_dto.games[0].uuid, quantity=1)
    api_client.add_to_cart(user_uuid, first_cart_item, x_task_value)
    second_cart_item = Cart(item_uuid=games_dto.games[1].uuid, quantity=1)
    api_client.add_to_cart(user_uuid, second_cart_item, x_task_value)

    api_client.delete_item_cart(user_uuid, games_dto.games[0].uuid, x_task_value)

    response = api_client.get_cart(user_uuid, x_task_value)
    order_dto = CartResponse(**response.json())
    assert order_dto.items, f"Partial deletion failed for user: {order_dto.user_uuid}"


@allure.feature("Cart API")
@allure.story("Flush users cart")
@pytest.mark.parametrize("x_task_value", ["api-15"])
def test_flush_cart(api_client, x_task_value):
    games = api_client.get_games(x_task_value)
    games_dto = GamesResponse(**games.json())
    users_response = api_client.get_users(x_task_value, 0)
    users_dto = Users(**users_response.json())

    user_uuid = users_dto.users[0].uuid

    cart_item = Cart(item_uuid=games_dto.games[0].uuid, quantity=1)
    api_client.add_to_cart(user_uuid, cart_item, x_task_value)

    response = api_client.clear_user_cart(user_uuid, x_task_value)
    order_dto = CartResponse(**response.json())
    assert not order_dto.items, f"Cart flush failed. Cart not empty: {order_dto.user_uuid}"


@allure.feature("Cart API")
@allure.story("Change item in cart")
@pytest.mark.parametrize("x_task_value", ["api-13"])
def test_change_item(api_client, x_task_value):
    games = api_client.get_games(x_task_value)
    games_dto = GamesResponse(**games.json())
    users_response = api_client.get_users(x_task_value, 0)
    users_dto = Users(**users_response.json())

    user_uuid = users_dto.users[0].uuid
    gamed_uuid = games_dto.games[0].uuid

    new_cart_item = Cart(item_uuid=gamed_uuid, quantity=1)

    api_client.add_to_cart(user_uuid, new_cart_item, x_task_value)

    changed_cart_item = Cart(item_uuid=gamed_uuid, quantity=2)

    response = api_client.change_item__cart(user_uuid, changed_cart_item, x_task_value)
    order_dto = CartResponse(**response.json())
    assert order_dto.items, f"Items in cart disappeared"
