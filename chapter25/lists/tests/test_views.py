import time
import unittest
from unittest.mock import Mock, patch

from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse
from django.utils.html import escape

from accounts.models import User
from lists.forms import DUPLICATE_ITEM_ERROR, ExistingListItemForm, ItemForm, EMPTY_ITEM_ERROR
from lists.models import Item, List
from lists.views import new_list


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_home_page_uses_item_form(self):
        response = self.client.get("/")
        self.assertIsInstance(response.context["form"], ItemForm)


class NewListViewIntegratedTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post("/lists/new", data={"text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.last()
        self.assertEqual(new_item.text, "A new list item")

    def test_for_invalid_input_doesnt_save_but_shows_errors(self):
        '''тест: недопустимый ввод не сохраняется, но показывает ошибки'''
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_list_owner_is_saved_if_user_is_authenticated(self):
        '''тест: владелец списка сохраняется, если
        пользователь аутентифицирован'''
        user = User.objects.create(email='a@b.com')
        self.client.force_login(user)
        self.client.post('/lists/new', data={'text': 'new item'})
        list_ = List.objects.first()
        self.assertEqual(list_.owner, user)


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        mylist = List.objects.create()
        response = self.client.get(f"/lists/{mylist.id}/")
        self.assertTemplateUsed(response, "list.html")

    def test_displays_item_form(self):
        mylist = List.objects.create()
        response = self.client.get(f"/lists/{mylist.id}/")
        self.assertIsInstance(response.context["form"], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text="itemey 1", list=correct_list)
        Item.objects.create(text="itemey 2", list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text="other list item", list=other_list)

        response = self.client.get(f"/lists/{correct_list.id}/")

        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")
        self.assertNotContains(response, "other list item")

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f"/lists/{correct_list.id}/")
        self.assertEqual(response.context["list"], correct_list)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f"/lists/{correct_list.id}/",
            data={"text": "A new item for an existing list"},
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.get()
        self.assertEqual(new_item.text, "A new item for an existing list")
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/",
            data={"text": "A new item for an existing list"},
        )

        self.assertRedirects(response, f"/lists/{correct_list.id}/")

    def post_invalid_input(self):
        mylist = List.objects.create()
        return self.client.post(
            f"/lists/{mylist.id}/",
            data={"text": ""},
        )

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list.html")

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context["form"], ExistingListItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='textey')
        response = self.client.post(
            f'/lists/{list1.id}/', data={'text': 'textey'}
        )

        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.count(), 1)


class MyListsTest(TestCase):
    def test_my_lists_url_renders_my_lists_template(self):
        User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com/')
        self.assertTemplateUsed(response, 'my_lists.html')

    def test_passes_correct_owner_to_template(self):
        User.objects.create(email='wrong@owner.com')
        correct_user = User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com/')
        self.assertEqual(response.context['owner'], correct_user)


@patch('lists.views.NewListForm')
@patch('lists.views.redirect')
class NewListViewUnitTests(unittest.TestCase):
    def setUp(self) -> None:
        self.request = HttpRequest()
        self.request.POST['text'] = 'new list item'
        self.request.user = Mock()
    
    def test_passes_POST_data_to_new_list_form(
        self, _, mock_new_list_form
    ):
        new_list(self.request)
        mock_new_list_form.assert_called_once_with(data=self.request.POST)

    def test_saves_form_with_owner_if_form_valid(
        self, _, mock_new_list_form
    ):
        mock_form = mock_new_list_form.return_value
        mock_form.is_valid.return_value = True
        new_list(self.request)
        mock_form.save.assert_called_once_with(owner=self.request.user)

    def test_redirects_to_form_returned_object_if_form_valid(
        self, mock_redirect, mock_new_list_form
    ):
        mock_form = mock_new_list_form.return_value
        mock_form.is_valid.return_value = True

        response = new_list(self.request)

        self.assertEqual(response, mock_redirect.return_value)
        mock_redirect.assert_called_once_with(mock_form.save.return_value)

    @patch('lists.views.render')
    def test_renders_home_template_with_form_if_form_invalid(
        self, mock_render, _, mock_new_list_form
    ):
        mock_form = mock_new_list_form.return_value
        mock_form.is_valid.return_value = False
        response = new_list(self.request)

        self.assertEqual(response, mock_render.return_value)

        mock_render.assert_called_once_with(
            self.request, 'home.html', {'form': mock_form}
        )

    def test_does_not_save_if_form_invalid(self, _, mock_new_list_form):
        mock_form = mock_new_list_form.return_value
        mock_form.is_valid.return_value = False
        new_list(self.request)
        self.assertFalse(mock_form.save.called)


class ShareListTest(TestCase):
    def test_post_redirects_to_lists_page(self):
        """Тест POST запрос переадресуется на главную страницу"""

        mylist = List.objects.create()
        share_list_url = reverse('share_list', kwargs={'list_id': mylist.id})

        response = self.client.post(share_list_url)

        self.assertRedirects(response, '/')
    
    def test_post_redirects_to_lists_page_with_list_owner(self):
        """
        Тест POST запрос с владельцем списка переадресует на страницу списка
        """
        owner = User.objects.create(email='hello@world.eu')
        mylist = List.objects.create(owner=owner)
        reverse_url = reverse('share_list', kwargs={'list_id': mylist.id})

        self.client.force_login(owner)
        response = self.client.post(reverse_url)

        self.assertRedirects(response, f'/lists/{mylist.id}/')

    def test_post_with_email_append_other_user_to_list(self):
        """
        Тест POST запрос с email добавляет этого пользователя в список
        """
        owner = User.objects.create(email='email@world.ru')
        list_ = List.objects.create(owner=owner)

        guest = User.objects.create(email='hello@world.eu')

        self.client.force_login(owner)
        self.client.post(
            reverse('share_list', kwargs={'list_id': list_.id}),
            {'sharee': guest.email}
        )
    
        self.assertIn(guest, list_.shared_with.all())
