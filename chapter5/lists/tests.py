import unittest
import os

import httpx


class HomePageTest(unittest.TestCase):
    """Тест домашней страницы"""
    HOME_PAGE_URL = 'http://localhost:8000'
    CLIENT = httpx.Client(base_url=HOME_PAGE_URL)

    def setUp(self) -> None:
        self.response = self.CLIENT.get('/')

    @classmethod
    def tearDownClass(cls):
        cls.CLIENT.close()

    def test_root_url_response(self) -> None:
        self.assertEqual(self.response.status_code, 200)

    def test_uses_home_template(self) -> None:
        html: str = self.response.text
        expected_html = open(
            f'{os.path.dirname(__file__)}/templates/home.html', 'r',
            encoding='utf-8'
        ).read().strip()
        self.assertEqual(html, expected_html)

    def test_can_save_a_POST_request(self) -> None:
        response = self.CLIENT.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.text)
