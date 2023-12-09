from fabric.api import run
from fabric.context_managers import settings

MANAGE_DOT_PY = '~/sites/{host}/virtualenv/bin/python ~/sites/{host}/source/manage.py'


def reset_database(host:  str) -> None:
    manage_dot_py = MANAGE_DOT_PY.format(host=host)
    with settings(host_string=f'root@{host}'):
        run(f'{manage_dot_py} flush --noinput')


def create_session_on_server(host: str, email: str) -> str:
    manage_dot_py = MANAGE_DOT_PY.format(host=host)
    with settings(host_string=f'root@{host}'):
        session_key = run(f'{manage_dot_py} create_session {email}')
        return session_key.strip()
