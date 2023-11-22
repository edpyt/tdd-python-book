from fastapi import APIRouter, Depends, Request

from depends import get_templates

router = APIRouter()


@router.get('/')
async def default_response(
    request: Request, templates=Depends(get_templates)
) -> dict[str, str]:
    return templates.TemplateResponse('main.html', {'request': request})
