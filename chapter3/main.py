from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from superlists.routes import router as superlists_router

app = FastAPI()

templates = Jinja2Templates(directory='templates')

app.include_router(superlists_router)
