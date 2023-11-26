from typing import Annotated

from fastapi import APIRouter, Depends, Request, Form

from depends import get_db_connection
from .depends import get_lists_templates
from .models import Item

router = APIRouter()


@router.get('/')
async def default_response(
    request: Request, templates=get_lists_templates()
):
    return templates.TemplateResponse('home.html', {'request': request})


@router.post('/', status_code=302)
def alter_form_search(
    request: Request,
    item_text: Annotated[str, Form()],
    session=Depends(get_db_connection),
    templates=get_lists_templates()
):
    Item.session = session
    item = Item()
    item.text = item_text
    item.save()
    return templates.TemplateResponse(
        'home.html', {'request': request, 'new_item_text': item_text}
    )
