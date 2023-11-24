from fastapi import FastAPI

from database import create_table
from depends import get_db_connection
from lists.routes import router as superlists_router

app = FastAPI()


@app.on_event('startup')
def start_db_table():
    conn = app.dependency_overrides.get(get_db_connection, get_db_connection)()
    create_table(conn)


app.include_router(superlists_router)
