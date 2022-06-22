import pytest


@pytest.fixture
def mock_env_creds(monkeypatch):
    mocked_env_variables = {
        "DB_HOST": "host1",
        "DB_USER": "user1",
        "DB_PASSWORD": "password1"
    }
    for k, v in mocked_env_variables.items():
        monkeypatch.setenv(k, v)
    return {
        "host": mocked_env_variables["DB_HOST"],
        "user": mocked_env_variables["DB_USER"],
        "password": mocked_env_variables["DB_PASSWORD"]
    }


@pytest.fixture
def mock_env_creds_not_setuped(monkeypatch):
    env_variables = {"DB_HOST", "DB_USER", "DB_PASSWORD"}
    for env_var in env_variables:
        monkeypatch.delenv(env_var)
    return {'host': None, 'password': None, 'user': None}
