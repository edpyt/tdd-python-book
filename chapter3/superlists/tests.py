import unittest

import httpx


class HomePageTest(unittest.TestCase):
    """Тест домашней страницы"""
    def test_root_url_response(self) -> None:
        response = httpx.get('http://localhost:8000/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_returns_correct_html(self) -> None:
        html: str = httpx.get('http://localhost:8000/').text
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.endswith('</html>'))
