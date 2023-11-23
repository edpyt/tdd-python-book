import unittest

import httpx

from lists.depends import get_lists_templates


class HomePageTest(unittest.TestCase):
    """Тест домашней страницы"""
    @classmethod
    def setUpClass(cls):
        cls.HOME_PAGE_URL = 'http://localhost:8000'
        cls.CLIENT = httpx.Client(base_url=cls.HOME_PAGE_URL)

    @classmethod
    def tearDownClass(cls):
        cls.CLIENT.close()

    def setUp(self) -> None:
        self.response = self.CLIENT.get('/')

    def test_root_url_response(self) -> None:
        self.assertEqual(self.response.status_code, 200)

    def test_uses_home_template(self) -> None:
        html: str = self.response.text

        templates = get_lists_templates()

        expected_html = templates.get_template('home.html').render()

        self.assertEqual(html, expected_html)

    def test_can_save_a_POST_request(self) -> None:
        response = self.CLIENT.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.text)
