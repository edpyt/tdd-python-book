import unittest

import httpx

from lists.depends import get_lists_templates
from lists.models import Item


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


class ItemModelTest(unittest.TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.all()
        self.assertEqual(len(saved_items), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')
