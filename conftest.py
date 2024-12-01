import os

import pytest
from filelock import FileLock

from api_handler.api_client import ApiClient

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


@pytest.fixture(scope="session")
def base_url(request):
    env = request.config.getoption("--env")
    url = ENVIRONMENTS.get(env)
    if not url:
        raise ValueError(f"Unknown environment: {env}. Available options are: {', '.join(ENVIRONMENTS.keys())}")
    return url


@pytest.fixture(scope="session")
def api_client(base_url):
    """
    Возвращает экземпляр API клиента с базовым URL.
    """
    return ApiClient(base_url=base_url)


@pytest.fixture(scope="session", autouse=True)
def setup_test(api_client, worker_id):
    lock_file = "setup.lock"

    # Один процесс (мастер)
    if worker_id == "master":
        if not os.path.exists(lock_file + ".done"):
            api_client.setup()
            with open(lock_file + ".done", "w") as f:
                f.write("done")
    # Многопроцессорность
    else:
        with FileLock(lock_file + ".lock"):
            if not os.path.exists(lock_file + ".done"):
                api_client.setup()
                with open(lock_file + ".done", "w") as f:
                    f.write("done")

    yield

    if os.path.exists(lock_file + ".lock"):
        os.remove(lock_file + ".lock")
    if os.path.exists(lock_file + ".done"):
        os.remove(lock_file + ".done")
