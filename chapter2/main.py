import sqlite3
from typing import Generator

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

connection = sqlite3.connect('db.sqlite3')

app = FastAPI()

templates = Jinja2Templates(directory='templates')


@app.get('/')
async def get_todos_page(request: Request):
    return templates.TemplateResponse('todo.html', {'request': request})
