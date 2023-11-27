import unittest
import sqlite3

from fastapi.testclient import TestClient

from depends import get_db_connection
from lists.depends import get_lists_templates
from lists.models import Item
from main import app


def override_get_db():
    return sqlite3.connect(
        'file::memory:?cache=shared',
        uri=True,
        check_same_thread=False
    )


app.dependency_overrides[get_db_connection] = override_get_db

Item.session = override_get_db()


class HomePageTest(unittest.TestCase):
    """Тест домашней страницы"""
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.HOME_PAGE_URL = 'http://localhost:8000'

    def setUp(self) -> None:
        self.response = self.client.get('/')

    def test_root_url_response(self) -> None:
        self.assertEqual(self.response.status_code, 200)

    def test_uses_home_template(self) -> None:
        html: str = self.response.text

        templates = get_lists_templates()

        expected_html = templates.get_template('home.html').render()

        self.assertEqual(html, expected_html)

    def test_can_save_a_POST_request(self) -> None:
        with TestClient(app):
            self.client.post(
                '/', data={'item_text': 'A new list item'}
            )
            self.assertEqual(len(Item.all()), 1)
            new_item = Item.first()
            self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self) -> None:
        response = self.client.post(
            '/',
            data={'item_text': 'A new list item'},
            allow_redirects=False
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['location'], '/')

    def test_only_saves_items_when_necessary(self):
        with TestClient(app):
            self.client.get('/')
            self.assertEqual(len(Item.all()), 3)

    def test_displays_all_list_items(self):
        Item.create('itemey 1')
        Item.create('itemey 2')

        response = self.client.get('/')
        print(response.content)


class ItemModelTest(unittest.TestCase):
    def test_get_item_by_id(self) -> None:
        with TestClient(app):
            my_item = Item()
            my_item.text = 'HAHAHAH'
            my_item.save()

    def test_saving_and_retrieving_items(self):
        with TestClient(app):
            first_item = Item()
            first_item.text = 'The first (ever) list item'
            first_item.save()

            second_item = Item()
            second_item.text = 'Item the second'
            second_item.save()

            saved_items = Item.all()
            self.assertEqual(len(saved_items), 7)
            first_saved_item, second_saved_item = saved_items[-2:]

            self.assertEqual(
                first_saved_item.text, 'The first (ever) list item'
            )
            self.assertEqual(second_saved_item.text, 'Item the second')
