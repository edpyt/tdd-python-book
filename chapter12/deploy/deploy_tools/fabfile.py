import asyncio
import os
import random

from fabric.contrib.files import append, exists, sed 
from fabric.api import env, local, run 

GITHUB_ACCESS_TOKEN_KEY = os.environ.get('GITHUB_ACCESS_TOKEN_KEY')
assert GITHUB_ACCESS_TOKEN_KEY, 'Provide GITHUB_ACCESS_TOKEN_KEY!'

REPO_URL = f'https://{GITHUB_ACCESS_TOKEN_KEY}@github.com/edpyt/tdd-python-book'


def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    source_folder = site_folder + '/source'
    asyncio.run(_deploy(source_folder))


async def _deploy(source_folder: str) -> None:
    await _get_latest_source(source_folder)
    tasks = [
        _update_settings(source_folder, env.host),
        _update_virtualenv(source_folder),
        _update_static_files(source_folder),
        _update_database(source_folder),
    ]
    await asyncio.gather(*tasks)


async def _get_latest_source(source_folder: str) -> None:
    if exists(source_folder + '/.git'):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')
    current_commit = local('git log -n 1 --format=%H', capture=True)
    run(f'cd {source_folder} && git reset --hard {current_commit}')


async def _update_settings(source_folder: str, site_name: str) -> None:
    settings_path = source_folder + '/superlists/settings.py'

    sed(settings_path, "DEBUG = True", "DEBUG = FALSE")
    sed(
        settings_path,
        'ALLOWED_HOSTS = .+$',
        f'ALLOWED_HOSTS = ["{site_name}"]'
    )
    
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


async def _update_virtualenv(source_folder: str) -> None:
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run(f'python3.11 -m venv {virtualenv_folder}')
    run(
        f'{virtualenv_folder}/bin/pip install -r {source_folder}/'
        'requirements.txt'
    )


async def _update_static_files(source_folder: str) -> None:
    run(
        f'cd {source_folder}'
        ' && ../virtualenv/bin/python manage.py collectstatic --noinput'
    )


async def _update_database(source_folder: str) -> None:
    run(
        f'cd {source_folder}'
        ' && ../virtualenv/bin/python manage.py migrate --noinput'
    )