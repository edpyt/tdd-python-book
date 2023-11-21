from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def main_page():
    return {'Hello': 'World'}


@app.get('/test')
async def test_paqe():
    return {'is_fastapi': True}
