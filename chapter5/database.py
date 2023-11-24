from abc import ABC, abstractmethod
import sqlite3


class Database(ABC):
    """
    Database context manager
    """
    def __init__(self, driver) -> None:
        self.driver = driver

    @abstractmethod
    def connect_to_database(self):
        raise NotImplementedError()

    def __enter__(self):
        self.connection = self.connect_to_database()
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exception_type, exc_val, traceback):
        self.cursor.close()
        self.connection.close()


class SqliteDatabase(Database):
    def __init__(self, conn) -> None:
        self.driver = sqlite3
        self._conn = conn
        super().__init__(self.driver)

    def connect_to_database(self):
        return self._conn


def create_table(conn):
    with SqliteDatabase(conn) as db:
        db.cursor.execute("""CREATE TABLE IF NOT EXISTS item (
            id integer PRIMARY KEY,
            text TEXT
            );
        """)
        db.connection.commit()
        print('tables created')
