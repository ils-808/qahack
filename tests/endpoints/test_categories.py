import pytest
import allure
from models.game_models import GamesResponse


@allure.feature("Categories API")
@allure.story("Get games by category")
@pytest.mark.parametrize("category_uuid, x_task_value", [("8126d35b-5336-41ad-981d-f245c3e05665", "api-10")])
def test_search_category_games(api_client, category_uuid, x_task_value):
    response = api_client.search_games_by_category(category_uuid, x_task_value)
    dto = GamesResponse(**response.json())

    assert category_uuid in dto.games[0].category_uuids, f"Category mismatch: {dto.games[0].title}"