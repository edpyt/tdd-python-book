import unittest
import os

import httpx


class HomePageTest(unittest.TestCase):
    """Тест домашней страницы"""
    def setUp(self):
        self.response = httpx.get('http://localhost:8000/')

    def test_root_url_response(self) -> None:
        self.assertEqual(self.response.status_code, 200)

    def test_home_page_returns_correct_html(self) -> None:
        html: str = self.response.text
        expected_html = open(
            f'{os.path.dirname(__file__)}/templates/home.html', 'r',
            encoding='utf-8'
        ).read().strip()
        self.assertEqual(html, expected_html)
