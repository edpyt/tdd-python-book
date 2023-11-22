from fastapi import FastAPI

from superlists.routes import router as superlists_router

app = FastAPI()


app.include_router(superlists_router)
