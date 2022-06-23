import pytest

from src.db import DbWrapper


class TestDbWrapperInit:

    def test_init(self):
        test_creds = {
            "host": "host1",
            "user": "user1",
            "password": "password1"
        }
        db_wrapper = DbWrapper(**test_creds)
        assert db_wrapper.__getattribute__("_host") == test_creds.get("host")
        assert db_wrapper.__getattribute__("_user") == test_creds.get("user")
        assert db_wrapper.__getattribute__("_password") == test_creds.get("password")
        assert db_wrapper.__getattribute__("_conn") is None

    @pytest.mark.parametrize("funct_kwargs", [{}, {
            "host": "host1"
        },
        {
            "host": "host1",
            "user": "user1"
        },
        {
            "host": "host1",
            "user": "user1",
            "password": "password1",
            "something": "something1"
        }])
    def test_init_incorrect_number_of_parameters(self, funct_kwargs):
        with pytest.raises(TypeError):
            DbWrapper(**funct_kwargs)

    @pytest.mark.parametrize("funct_kwargs", [{
            "host": "host1",
            "user": "user1",
            "password": 123456
        },
        {
            "host": "host1",
            "user": None,
            "password": "password1"
        },
        {
            "host": range(1),
            "user": "user1",
            "password": "password1"
        }])
    def test_init_incorrect_type_of_parameters(self, funct_kwargs):
        with pytest.raises(TypeError):
            DbWrapper(**funct_kwargs)


# Below I would need to more time for:
# - upskill myself around Mocking DB options and generally Mocking area
# So skipping for now


class TestDbWrapperContextManager:
    pass


class TestDbWrapperExecuteQuery:
    pass


class TestDbWrapperInitiateDb:
    pass


class TestDbWrapperDropDb:
    pass
