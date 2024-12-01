from datetime import datetime

from pydantic import BaseModel
from typing import List, Optional, Literal


class Game(BaseModel):
    uuid: str
    title: str
    price: int
    category_uuids: List[str]


class GameWishlist(BaseModel):
    items: List[Game]
    user_uuid: Optional[str] = None


class Meta(BaseModel):
    total: int


class GamesResponse(BaseModel):
    games: List[Game]
    meta: Meta


class Category(BaseModel):
    uuid: str
    name: str


#
#
# class Order(BaseModel):
#     uuid: str
#     total_price: int
#     status: str


class Review(BaseModel):
    uuid: str
    title: str
    body: str
    score: int


class Payment(BaseModel):
    uuid: str
    amount: int
    status: str


class UserBase(BaseModel):
    uuid: Optional[str] = None
    nickname: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = "\"HA\"R\"HA\"R"
    phone: Optional[str] = None
    userStatus: Optional[int] = None
    avatar_url: Optional[str] = None


class Users(BaseModel):
    users: List[UserBase]
    meta: Meta


class Cart(BaseModel):
    item_uuid: Optional[str] = None
    quantity: int


class ItemCart(BaseModel):
    item_uuid: Optional[str] = None
    quantity: int
    total_price: int


class CartResponse(BaseModel):
    items: List[ItemCart]
    total_price: int
    user_uuid: Optional[str] = None


class OrderItem(BaseModel):
    item_uuid: Optional[str] = None
    quantity: int


class OrderItemList(BaseModel):
    items: List[OrderItem]


class Order(BaseModel):
    created_at: datetime
    items: List[ItemCart]
    status: str
    total_price: int
    updated_at: datetime
    user_uuid: Optional[str] = None
    uuid: Optional[str] = None


class OrdersResponse(BaseModel):
    meta: Meta
    orders: List[Order]


class PaymentRequest(BaseModel):
    order_uuid: Optional[str] = None
    payment_method: Literal['card', 'cash', 'bank_transfer']


class PaymentResponse(BaseModel):
    amount: int
    created_at: datetime
    order_uuid: Optional[str] = None
    payment_method: Literal['card', 'cash', 'bank_transfer']
    status: Literal['processing', 'completed', 'failed']
    updated_at: datetime
    user_uuid: Optional[str] = None
    uuid: Optional[str] = None

class Payments(BaseModel):
    meta: Meta
    payments: List[PaymentResponse]
