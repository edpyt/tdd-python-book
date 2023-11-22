from fastapi.templating import Jinja2Templates


def get_lists_templates():
    return Jinja2Templates(directory='lists/templates')

