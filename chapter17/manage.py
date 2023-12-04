#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'superlists.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            'available on your PYTHONPATH environment variable? Did you '
            'forget to activate a virtual environment?'
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    if 'fastwsgi' in sys.argv:
        import fastwsgi

        from superlists.wsgi import get_wsgi_application
        fastwsgi.run(wsgi_app=get_wsgi_application(), host='0.0.0.0', port=8000)
    else:
        main()
