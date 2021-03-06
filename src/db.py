from mysql import connector
from mysql.connector.errors import OperationalError

from src.helpers import LogProvider


class DbWrapper:
    def __init__(self, host: str, user: str, password: str):
        try:
            # will raise Type Error if not all params are str
            "".join([v for k, v in locals().items() if k != "self"])
        except TypeError:
            raise
        self._host = host
        self._user = user
        self._password = password
        self._conn = None
        self._logger = LogProvider()

    def __enter__(self):
        try:
            self._conn = connector.connect(
                host=self._host, user=self._user, password=self._password
            )
        except OperationalError as err:
            self._logger.exception(
                f"Connecting with Database was not possible due to: {err}"
            )
            raise OperationalError from err
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._conn.close()

    def execute_query(self, query: str) -> None:
        self._logger.debug(f"Executing query:\n{query}")
        try:
            self._conn.cursor().execute(query)
        except OperationalError as err:
            self._logger.exception(
                f"Connecting with Database was not possible due to: {err}"
            )
            self._logger.debug(query)
            raise OperationalError from err

    def initiate_db(self) -> None:
        with open("src/static/dbschema.sql", "r", encoding="UTF-8") as schema:
            self.execute_query(schema.read())

    def drop_db(self) -> None:
        with open("src/static/dbdrop.sql", "r", encoding="UTF-8") as schema:
            self.execute_query(schema.read())

    def select_query(self, query: str) -> list[tuple[str, ...], ...]:
        self._logger.debug(f"Executing query:\n{query}")
        try:
            mycursor = self._conn.cursor()
            mycursor.execute(query)
            return mycursor.fetchall()
        except OperationalError as err:
            self._logger.exception(
                f"Connecting with Database was not possible due to: {err}"
            )
            self._logger.debug(query)
            raise OperationalError from err


if __name__ == "__main__":
    pass
