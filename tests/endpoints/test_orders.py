import pytest
import allure
from models.game_models import GamesResponse, Users, GameWishlist, OrderItemList, OrderItem, OrdersResponse


@allure.feature("Orders API")
@allure.story("Duplicate item in order")
@pytest.mark.parametrize("x_task_value", ["api-16"])
def test_add_item_wishlist(api_client, x_task_value):
    users_response = api_client.get_users(x_task_value, 0)
    users_dto = Users(**users_response.json())

    user_uuid = users_dto.users[0].uuid

    games = api_client.get_games(x_task_value)
    games_dto = GamesResponse(**games.json())
    game_uuid = games_dto.games[0].uuid

    order_data = OrderItemList(items=[
        OrderItem(item_uuid=game_uuid, quantity=1),
        OrderItem(item_uuid=game_uuid, quantity=1),
    ])

    response = api_client.order_create(user_uuid, order_data.dict(), x_task_value)

    assert response.status_code == 400, "Duplicate items in order"


@allure.feature("Orders API")
@allure.story("Limit list user's orders")
@pytest.mark.parametrize("x_task_value", ["api-17"])
def test_orders_limit(api_client, x_task_value):
    users_response = api_client.get_users(x_task_value, 0)
    users_dto = Users(**users_response.json())

    user_uuid = users_dto.users[1].uuid

    games = api_client.get_games(x_task_value)
    games_dto = GamesResponse(**games.json())
    game_uuid = games_dto.games[0].uuid

    order_data = OrderItemList(items=[
        OrderItem(item_uuid=game_uuid, quantity=1)
    ])

    api_client.order_create(user_uuid, order_data.dict(), x_task_value)
    api_client.order_create(user_uuid, order_data.dict(), x_task_value)
    limit = 1
    response = api_client.orders(user_uuid, limit, x_task_value)
    orders = OrdersResponse(**response.json())
    assert len(orders.orders) == limit, f"Was displayed {len(orders.orders)} orders instead of {limit}"



@allure.feature("Orders API")
@allure.story("Change order status")
@pytest.mark.parametrize("status, x_task_value", [("canceled", "api-18")])
def test_change_order_status(api_client, status, x_task_value):
    users_response = api_client.get_users(x_task_value, 0)
    users_dto = Users(**users_response.json())

    user_uuid = users_dto.users[1].uuid

    games = api_client.get_games(x_task_value)
    games_dto = GamesResponse(**games.json())
    game_uuid = games_dto.games[0].uuid

    order_data = OrderItemList(items=[
        OrderItem(item_uuid=game_uuid, quantity=1)
    ])

    api_client.order_create(user_uuid, order_data.dict(), x_task_value)
    limit = 1
    create_response = api_client.orders(user_uuid, limit, x_task_value)
    orders = OrdersResponse(**create_response.json())

    response = api_client.order_change_status(orders.orders[0].uuid, status, x_task_value)

    assert response.status_code == 200, f"Failed to change order status {orders.orders[0].uuid}"
