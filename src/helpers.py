from datetime import datetime
from os import getenv
from pathlib import Path
from typing import Iterator, Union
from logging import (basicConfig, getLogger, DEBUG)

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


def build_transaction(sql_query: str) -> str:
    return f"START TRANSACTION;\nUSE `mydb`;\n{sql_query}\nCOMMIT;"


def build_update_currency_transaction(currency: str, value: float) -> str:
    if currency == "USD":
        update_sql_query = f"UPDATE Product SET UnitPriceUSD='{value}';"
    elif currency == "Euro":
        update_sql_query = f"UPDATE Product SET UnitPriceEuro='{value}';"
    else:
        raise ValueError("Sql could not be built.")

    return build_transaction(update_sql_query)


def get_file_content(file_path: Union[str, Path]) -> str:
    with open(file_path, "r", encoding="UTF-8") as file_obj:
        return file_obj.read()


def get_timestamp():
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    time = now.strftime("%H%M%S")
    return year + month + day + "_" + time


class LogProvider:
    """ Singleton class. """
    logger = None

    def __new__(cls):
        if cls.logger is None:
            format_ = "{asctime} {levelname} {message}"
            basicConfig(filename=f"Log{get_timestamp()}.log", level=DEBUG, format=format_, style='{')
            cls.logger = getLogger()
        return cls.logger
