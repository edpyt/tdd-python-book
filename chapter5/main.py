from fastapi import FastAPI

from database import create_table
from lists.routes import router as superlists_router

app = FastAPI()


@app.on_event('startup')
def start_db_table():
    create_table()


app.include_router(superlists_router)
