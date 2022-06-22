import mysql.connector

from src.helpers import get_credentials, transaction_reader


class DbWrapper:

    def __init__(self, host: str, user: str, password: str):
        self._host = host
        self._user = user
        self._password = password
        self._conn = None

    def __enter__(self):
        self._conn = mysql.connector.connect(**get_credentials())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._conn.close()

    def execute_query(self, query: str) -> None:
        self._conn.cursor().execute(query)

    def initiate_db(self) -> None:
        with open("src/static/dbschema.sql", "r", encoding="UTF-8") as schema:
            self.execute_query(schema.read())

    def drop_db(self) -> None:
        with open("src/static/dbdrop.sql",  "r", encoding="UTF-8") as schema:
            self.execute_query(schema.read())


def populate_db() -> None:
    for transaction in transaction_reader():
        with DbWrapper(**get_credentials()) as dbtemp:
            dbtemp.execute_query(transaction)


if __name__ == "__main__":
    with DbWrapper(**get_credentials()) as db:
        db.drop_db()
        db.initiate_db()
    populate_db()
