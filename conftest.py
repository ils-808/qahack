import pytest
from api_handler.ApiClient import ApiClient

# Конфигурация URL для разных сред
ENVIRONMENTS = {
    "dev": "https://dev-gs.qa-playground.com/api/v1",
    "prod": "https://release-gs.qa-playground.com/api/v1"
}


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Environment to run tests against (e.g., dev, prod, staging)"
    )


@pytest.fixture
def base_url(request):
    env = request.config.getoption("--env")
    url = ENVIRONMENTS.get(env)
    if not url:
        raise ValueError(f"Unknown environment: {env}. Available options are: {', '.join(ENVIRONMENTS.keys())}")
    return url


@pytest.fixture()
def api_client(base_url):
    """
    Возвращает экземпляр API клиента с базовым URL.
    """
    return ApiClient(base_url=base_url)
