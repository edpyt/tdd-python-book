from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from .depends import get_lists_templates

router = APIRouter()


@router.get('/')
async def default_response(
    request: Request, templates=Depends(get_lists_templates)
):
    return templates.TemplateResponse('home.html', {'request': request})


@router.post('/')
async def alter_form_search():
    return RedirectResponse('/', status_code=302)
