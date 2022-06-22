from os import getenv
from typing import Iterator

from dotenv import load_dotenv


def get_credentials() -> dict:
    load_dotenv()
    return {
        "host": getenv("DB_HOST"),
        "user": getenv("DB_USER"),
        "password": getenv("DB_PASSWORD")
        }


def transaction_reader() -> Iterator[str]:
    with open("src/static/population.sql", "r", encoding="UTF-8") as transactions_file:
        for line in transactions_file:
            if "INSERT INTO" in line:
                yield f"START TRANSACTION;\nUSE `mydb`;\n{line}\nCOMMIT;"
