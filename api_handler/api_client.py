import logging

import requests
from typing import Optional, Dict
from data import BASE_HEADERS
from models.game_models import UserBase, Cart, OrderItemList, PaymentRequest
from utils import get_path


class ApiClient:
    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None):
        """
        Инициализация API клиента.

        :param base_url: Базовый URL для API.
        :param headers: Общие заголовки для всех запросов.
        """
        self.base_url = base_url
        self.headers = BASE_HEADERS
        self.logger = logging.getLogger("ApiClient")
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(handler)

    def log_request(self, method: str, url: str, headers: Dict[str, str], params: Optional[Dict] = None,
                    data: Optional[Dict] = None):
        """
        Логирует информацию о запросе.
        """
        self.logger.info(f"Request: {method} {url}")
        self.logger.info(f"Headers: {headers}")
        if params:
            self.logger.info(f"Params: {params}")
        if data:
            self.logger.info(f"Body: {data}")

    def log_response(self, response: requests.Response):
        """
        Логирует информацию об ответе.
        """
        self.logger.info(f"Response [{response.status_code}]: {response.text}")

    def setup(self, ):
        url = f"{self.base_url}/setup"

        self.logger.info(f"Request: POST {url} | Headers: {self.headers}")
        response = requests.post(url, headers=self.headers)
        self.logger.info(f"Response [{response.status_code}]: {response.text}")
        return response

    def search_game_by_name(self, search, headers):
        url = f"{self.base_url}/games/search"

        self.headers.update({"X-Task-Id": f"{headers}"})
        params = {"query": search, "offset": 0, "limit": 10}
        self.logger.info(f"Request: GET {url} | Params: {params} | Headers: {self.headers}")
        response = requests.get(url, headers=self.headers, params=params)
        self.logger.info(f"Response [{response.status_code}]: {response.text}")
        return response

    def search_games_by_category(self, search, headers):
        url = f"{self.base_url}/categories/{search}/games"
        self.headers.update({"X-Task-Id": f"{headers}"})
        params = {"query": search, "offset": 0, "limit": 10}
        self.logger.info(f"Request: GET {url} | Params: {params} | Headers: {self.headers}")
        response = requests.get(url, headers=self.headers, params=params)
        self.logger.info(f"Response [{response.status_code}]: {response.text}")
        return response

    def get_games(self, headers, game_uuid_list=None):
        url = f"{self.base_url}/games"
        self.headers.update({"X-Task-Id": f"{headers}"})
        params = {"query": game_uuid_list, "offset": 0, "limit": 10}
        self.logger.info(f"Request: GET {url} | Params: {params} | Headers: {self.headers}")
        response = requests.get(url, headers=self.headers, params=params)
        self.logger.info(f"Response [{response.status_code}]: {response.text}")
        return response

    def get_game(self, game_uuid, headers):
        url = f"{self.base_url}/games/{game_uuid}"

        self.headers.update({"X-Task-Id": f"{headers}"})
        self.logger.info(f"Request: GET {url} | Headers: {self.headers}")
        response = requests.get(url, headers=self.headers)
        self.logger.info(f"Response [{response.status_code}]: {response.text}")
        return response

    def create_user(self, user_data: UserBase, headers):
        url = f"{self.base_url}/users"

        self.headers.update({"X-Task-Id": f"{headers}"})
        self.logger.info(f"Request: POST {url} | Headers: {self.headers}")
        response = requests.post(url, headers=self.headers, json=user_data.model_dump())
        self.logger.info(f"Response [{response.status_code}]: {response.text}")
        return response

    def get_users(self, headers, offset):
        url = f"{self.base_url}/users"

        self.headers.update({"X-Task-Id": f"{headers}"})
        params = {"offset": offset, "limit": 10}
        self.logger.info(f"Request: GET {url} | Headers: {self.headers}")
        response = requests.get(url, headers=self.headers, params=params)
        self.logger.info(f"Response [{response.status_code}]: {response.text}")
        return response

    def get_user(self, user_uuid, headers):
        url = f"{self.base_url}/users/{user_uuid}"

        self.headers.update({"X-Task-Id": f"{headers}"})
        self.logger.info(f"Request: GET {url} | Headers: {self.headers}")
        response = requests.get(url, headers=self.headers)
        self.logger.info(f"Response [{response.status_code}]: {response.text}")
        return response

    def delete_user(self, user_uuid, headers):
        url = f"{self.base_url}/users/{user_uuid}"

        self.headers.update({"X-Task-Id": f"{headers}"})
        self.logger.info(f"Request: DELETE {url} | Headers: {self.headers}")
        response = requests.delete(url, headers=self.headers)
        self.logger.info(f"Response [{response.status_code}]: {response.text}")
        return response

    def patch_user(self, user_data: UserBase, user_uuid, headers):
        url = f"{self.base_url}/users/{user_uuid}"

        self.headers.update({"X-Task-Id": f"{headers}"})
        self.logger.info(f"Request: PATCH {url} | Headers: {self.headers}")
        response = requests.patch(url, headers=self.headers, json=user_data.model_dump())
        self.logger.info(f"Response [{response.status_code}]: {response.text}")
        return response

    def auth_user(self, user_data: UserBase, headers):
        url = f"{self.base_url}/users/login"

        self.headers.update({"X-Task-Id": f"{headers}"})
        self.logger.info(f"Request: POST {url} | Headers: {self.headers}")
        response = requests.post(url, headers=self.headers, json=user_data.model_dump())
        self.logger.info(f"Response [{response.status_code}]: {response.text}")
        return response

    def upload_avatar(self, user_uuid, file_name, file_content, headers):
        url = f"{self.base_url}/users/{user_uuid}/avatar"

        print("create files object")
        files = {
            ('avatar_file', (file_name, file_content, 'image/jpeg'))
        }
        print("created files object")

        self.headers.update({"X-Task-Id": f"{headers}"})
        self.logger.info(f"Request: PUT {url} | Headers: {self.headers}")
        try:
            response = requests.put(url, headers=self.headers, files=files, timeout=15)
            response.raise_for_status()
            self.logger.info(f"Response [{response.status_code}]: {response.text}")
            return response
        except requests.exceptions.Timeout:
            print("Превышено время ожидания запроса.")
        except requests.exceptions.ConnectionError:
            print("Ошибка подключения к серверу.")
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP ошибка: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Произошла ошибка в запросе: {req_err}")


    def check_file_availability(self, file_url):
        """
        Проверяет доступность файла по указанному URL.

        :param file_url: URL файла для проверки.
        :return: Булево значение, доступен ли файл.
        """

        self.logger.info(f"Request: GET {file_url} | Headers: {self.headers}")
        response = requests.get(file_url)
        self.logger.info(f"Response [{response.status_code}]: {response.text}")
        return response

    def get_cart(self, user_uuid, headers):
        url = f"{self.base_url}/users/{user_uuid}/cart"

        self.headers.update({"X-Task-Id": f"{headers}"})
        self.logger.info(f"Request: GET {url} | Headers: {self.headers}")
        response = requests.get(url, headers=self.headers)
        self.logger.info(f"Response [{response.status_code}]: {response.text}")
        return response

    def add_to_cart(self, user_uuid, cart: Cart, headers):
        url = f"{self.base_url}/users/{user_uuid}/cart/add"

        self.headers.update({"X-Task-Id": f"{headers}"})
        self.logger.info(f"Request: POST {url} | Headers: {self.headers}")
        response = requests.post(url, headers=self.headers, json=cart.model_dump())
        self.logger.info(f"Response [{response.status_code}]: {response.text}")
        return response

    def delete_item_cart(self, user_uuid, item_uuid, headers):
        url = f"{self.base_url}/users/{user_uuid}/cart/remove"

        self.headers.update({"X-Task-Id": f"{headers}"})
        self.logger.info(f"Request: POST {url} | Headers: {self.headers}")
        response = requests.post(url, headers=self.headers, json={
            'item_uuid': item_uuid
        })
        self.logger.info(f"Response [{response.status_code}]: {response.text}")
        return response

    def clear_user_cart(self, user_uuid, headers):
        url = f"{self.base_url}/users/{user_uuid}/cart/clear"

        self.headers.update({"X-Task-Id": f"{headers}"})
        self.logger.info(f"Request: POST {url} | Headers: {self.headers}")
        response = requests.post(url, headers=self.headers)
        self.logger.info(f"Response [{response.status_code}]: {response.text}")
        return response

    def change_item__cart(self, user_uuid, cart: Cart, headers):
        url = f"{self.base_url}/users/{user_uuid}/cart/change"

        self.headers.update({"X-Task-Id": f"{headers}"})
        self.logger.info(f"Request: POST {url} | Headers: {self.headers}")
        response = requests.post(url, headers=self.headers, json=cart.model_dump())
        self.logger.info(f"Response [{response.status_code}]: {response.text}")
        return response

    def get_whishlist(self, user_uuid, headers):
        url = f"{self.base_url}/users/{user_uuid}/wishlist"

        self.headers.update({"X-Task-Id": f"{headers}"})
        self.logger.info(f"Request: GET {url} | Headers: {self.headers}")
        response = requests.get(url, headers=self.headers)
        self.logger.info(f"Response [{response.status_code}]: {response.text}")
        return response

    def add_item_whishlist(self, user_uuid, item_uuid, headers):
        url = f"{self.base_url}/users/{user_uuid}/wishlist/add"

        self.headers.update({"X-Task-Id": f"{headers}"})
        self.logger.info(f"Request: POST {url} | Headers: {self.headers}")
        response = requests.post(url, headers=self.headers, json={
            'item_uuid': item_uuid
        })
        self.logger.info(f"Response [{response.status_code}]: {response.text}")
        return response

    def delete_item_whishlist(self, user_uuid, item_uuid, headers):
        url = f"{self.base_url}/users/{user_uuid}/wishlist/remove"

        self.headers.update({"X-Task-Id": f"{headers}"})
        self.logger.info(f"Request: POST {url} | Headers: {self.headers}")
        response = requests.post(url, headers=self.headers, json={
            'item_uuid': item_uuid
        })
        self.logger.info(f"Response [{response.status_code}]: {response.text}")
        return response

    def order_create(self, user_uuid, order: OrderItemList, headers):
        url = f"{self.base_url}/users/{user_uuid}/orders"

        self.headers.update({"X-Task-Id": f"{headers}"})
        self.logger.info(f"Request: POST {url} | Headers: {self.headers}")
        response = requests.post(url, headers=self.headers, json=order)
        self.logger.info(f"Response [{response.status_code}]: {response.text}")
        return response

    def orders(self, user_uuid, limit, headers):
        url = f"{self.base_url}/users/{user_uuid}/orders"
        self.headers.update({"X-Task-Id": f"{headers}"})
        params = {"offset": 0, "limit": limit}
        self.logger.info(f"Request: GET {url} | Headers: {self.headers}")
        response = requests.get(url, headers=self.headers, params=params)
        self.logger.info(f"Response [{response.status_code}]: {response.text}")
        return response

    def order_change_status(self, order_uuid, status, headers):
        url = f"{self.base_url}/orders/{order_uuid}/status"

        self.headers.update({"X-Task-Id": f"{headers}"})
        self.logger.info(f"Request: PATCH {url} | Headers: {self.headers}")
        response = requests.patch(url, headers=self.headers, json={
            "status": status
        })
        self.logger.info(f"Response [{response.status_code}]: {response.text}")
        return response

    def create_payment(self, user_uuid, payment: PaymentRequest, headers):
        url = f"{self.base_url}/users/{user_uuid}/payments"

        self.headers.update({"X-Task-Id": f"{headers}"})
        self.logger.info(f"Request: POST {url} | Headers: {self.headers}")
        response = requests.post(url, headers=self.headers, json=payment.model_dump())
        self.logger.info(f"Response [{response.status_code}]: {response.text}")
        return response

    def get_payment(self, payment_uuid, headers):
        url = f"{self.base_url}/payments/{payment_uuid}"

        self.headers.update({"X-Task-Id": f"{headers}"})
        self.logger.info(f"Request: GET {url} | Headers: {self.headers}")
        response = requests.get(url, headers=self.headers)
        self.logger.info(f"Response [{response.status_code}]: {response.text}")
        return response
