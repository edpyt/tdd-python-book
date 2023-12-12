import time
from django.contrib.auth import get_user_model
from selenium.webdriver.common.by import By

from .base import FunctionalTest
from .list_page import ListPage
from .my_lists_page import MyListsPage

User = get_user_model()


class MyListsTest(FunctionalTest):
    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        self.create_pre_authenticated_session('edith@example.com')
        
        self.browser.get(self.live_server_url)
        self.add_list_item('Reticulate splines')
        self.add_list_item('Immanetize eschaton')
        first_list_url = self.browser.current_url

        list_page = ListPage(self).click_and_wait_for(
            self.browser.find_element(By.LINK_TEXT, 'My lists'),
            lambda: self.browser.find_element(By.LINK_TEXT, 'Reticulate splines')
        )

        list_page.click_and_wait_for(
            self.browser.find_element(By.LINK_TEXT, 'Reticulate splines'),
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        self.browser.get(self.live_server_url)
        list_page = ListPage(self)

        self.add_list_item('Click cows')
        second_list_url = self.browser.current_url

        list_page.click_and_wait_for(
            self.browser.find_element(By.LINK_TEXT, 'My lists'),
            lambda: self.browser.find_element(By.LINK_TEXT, 'Click cows')
        )

        list_page.click_and_wait_for(
            self.browser.find_element(By.LINK_TEXT, 'Click cows'),
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        list_page.click_and_wait_for(
            self.browser.find_element(By.LINK_TEXT, 'Log out'),
            lambda: self.assertEqual(
                self.browser.find_elements(By.LINK_TEXT, 'My lists'),
                []
            )
        )

    def test_list_owner_and_usage_permission(self):
        self.create_pre_authenticated_session('test@mail.com')

        self.browser.get(self.live_server_url)
        self.add_list_item('Hello')

        time.sleep(10)