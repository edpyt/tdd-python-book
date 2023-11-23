from typing import Annotated

from fastapi import APIRouter, Request, Form

from .depends import get_lists_templates

router = APIRouter()


@router.get('/')
async def default_response(
    request: Request, templates=get_lists_templates()
):
    return templates.TemplateResponse('home.html', {'request': request})


@router.post('/')
async def alter_form_search(
    request: Request,
    item_text: Annotated[str, Form()],
    templates=get_lists_templates()
):
    return templates.TemplateResponse(
        'home.html', {'request': request, 'new_item_text': item_text}
    )
