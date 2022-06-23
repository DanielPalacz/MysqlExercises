from os import getenv
from pathlib import Path
from typing import Iterator, Union

from dotenv import load_dotenv


load_dotenv()


def get_credentials() -> dict:

    db_host = getenv("DB_HOST")
    db_user = getenv("DB_USER")
    db_password = getenv("DB_PASSWORD")

    if db_host is None or db_user is None or db_password is None:
        raise OSError("Environment is not set.")

    return {
        "host": db_host,
        "user": db_user,
        "password": db_password
        }


def transaction_reader(transactions_path="src/static/population.sql") -> Iterator[str]:
    """Used only for initial db population."""
    with open(transactions_path, "r", encoding="UTF-8") as transactions_file:
        for line in transactions_file:
            if "INSERT INTO" in line:
                yield f"START TRANSACTION;\nUSE `mydb`;\n{line}\nCOMMIT;"


def get_file_content(file_path: Union[str, Path]) -> str:
    with open(file_path, "r", encoding="UTF-8") as file_obj:
        return file_obj.read()
