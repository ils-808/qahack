import pytest
import allure
from pydantic import ValidationError

from models.game_models import GamesResponse, Users, GameWishlist, OrderItemList, OrderItem, OrdersResponse, Order, \
    PaymentRequest, PaymentResponse


@allure.feature("Orders API")
@allure.story("Duplicate item in order")
@pytest.mark.parametrize("x_task_value", ["api-19"])
def test_validate_payment(api_client, x_task_value):
    users_response = api_client.get_users(x_task_value, 0)
    users_dto = Users(**users_response.json())

    user_uuid = users_dto.users[0].uuid

    games = api_client.get_games(x_task_value)
    games_dto = GamesResponse(**games.json())
    game_uuid = games_dto.games[0].uuid

    order_data = OrderItemList(items=[
        OrderItem(item_uuid=game_uuid, quantity=1)
    ])

    create_order = api_client.order_create(user_uuid, order_data.dict(), x_task_value)
    orders = Order(**create_order.json())
    order_uuid = orders.uuid

    payment = PaymentRequest(order_uuid=order_uuid, payment_method="card")

    payment_response = api_client.create_payment(user_uuid, payment, x_task_value)
    payment = PaymentResponse(**payment_response.json())
    get_payments = api_client.get_payment(payment.uuid, x_task_value)

    try:
        PaymentResponse(**get_payments.json())
    except ValidationError as e:
        print("ValidationError:", e)
        assert False, f"Response validation failed: {e}"
    assert True

