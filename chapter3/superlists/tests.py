import asyncio
import unittest

import httpx

from .routes import default_response


class HomePageTest(unittest.TestCase):
    """Тест домашней страницы"""
    def test_root_url_response(self) -> None:
        response = httpx.get('http://localhost:8000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), asyncio.run(default_response()))
