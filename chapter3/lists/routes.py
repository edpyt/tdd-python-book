from fastapi import APIRouter, Depends, Request

from .depends import get_lists_templates

router = APIRouter()


@router.get('/')
async def default_response(
    request: Request, templates=Depends(get_lists_templates)
) -> dict[str, str]:
    return templates.TemplateResponse('home.html', {'request': request})
