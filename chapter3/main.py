from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates


app = FastAPI()

templates = Jinja2Templates(directory='templates')


@app.get('/')
async def get_todos_page(request: Request):
    return templates.TemplateResponse('todo.html', {'request': request})
