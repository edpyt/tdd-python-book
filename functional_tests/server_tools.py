"""Works only with Docker"""
import pathlib
from typing import Any, Callable

from python_on_whales import DockerClient

DOCKER_DJANGO_CONTAINER_SERVICE = 'django'
MANAGE_DOT_PY = 'python manage.py'

COMPOSE_FILE = (
    pathlib.Path(__file__).parent.parent.resolve() /
    'deploy/subdomain/docker-compose.subdomain.yml'
)

def get_docker_client() -> DockerClient:
    return DockerClient(compose_files=[COMPOSE_FILE])


def docker_compose_execute(fn: Callable):
    docker = get_docker_client()
    
    def run_command(*args, **kwargs) -> Any:
        command: list[str] = fn(*args, **kwargs)
        response = docker.compose.execute(
            DOCKER_DJANGO_CONTAINER_SERVICE, command, tty=False
        )
        print(f'Execute command: {fn.__name__}')
        return response
    return run_command


@docker_compose_execute
def reset_database() -> list[str]:
    return MANAGE_DOT_PY.split() + ['flush', '--noinput']


@docker_compose_execute
def create_session_on_server(email: str) -> list[str]:
    return MANAGE_DOT_PY.split() + ['create_session', email]
    
