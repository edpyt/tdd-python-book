import httpx

response_json = httpx.get('http://localhost:8000/test').json()
assert response_json['is_fastapi']
