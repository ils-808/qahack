import pytest
import allure
from models.game_models import GamesResponse


@allure.feature("Games API")
@allure.story("Search games")
@pytest.mark.parametrize("search, x_task_value", [("Atomic Heart", "api-2")])
def test_search_games(api_client, search, x_task_value):
    response = api_client.search_game_by_name(search, x_task_value)
    dto = GamesResponse(**response.json())

    assert len(dto.games) == 1
    assert dto.games[0].title == search, f"Found game name doesn't match: {dto.games[0].title}"


@allure.feature("Games API")
@allure.story("Get a game by uuid")
@pytest.mark.parametrize("game_uuid, x_task_value", [("03dbad48-ad81-433d-9901-dd5332f5d9ee", "api-9")])
def test_get_games(api_client, game_uuid, x_task_value):
    response = api_client.get_game(game_uuid, x_task_value)

    assert response.status_code == 200, f"Seach game_uuid: {game_uuid} wasn't found. Response code: {response.status_code}"
