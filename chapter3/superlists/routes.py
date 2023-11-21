from fastapi import APIRouter

router = APIRouter()


@router.get('/')
async def default_response() -> dict[str, str]:
    return {'message': 'Hello'}
