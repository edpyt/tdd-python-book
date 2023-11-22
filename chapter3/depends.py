import sqlite3
from typing import Generator

from fastapi.templating import Jinja2Templates


def get_templates():
    return Jinja2Templates(directory='templates')


def get_db_connection() -> Generator:
    yield sqlite3.connect('db.sqlite3')
