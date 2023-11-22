import sqlite3
from typing import Generator


def get_db_connection() -> Generator:
    yield sqlite3.connect('db.sqlite3')
