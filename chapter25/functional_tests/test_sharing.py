import time
from selenium import webdriver
from selenium.webdriver.common.by import By

from .base import FunctionalTest
from .list_page import ListPage
from .my_lists_page import MyListsPage


def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        pass


class SharingTest(FunctionalTest):
    '''Тест обмена данными'''

    def test_can_share_a_list_with_another_user(self):
        self.create_pre_authenticated_session('edith@example.com')
        edith_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(edith_browser))
    
        oni_browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(oni_browser))
        self.browser = oni_browser
        user_email_share = 'oniciferous@example.com' 
        self.create_pre_authenticated_session(user_email_share)
        
        self.browser = edith_browser
        self.browser.get(self.live_server_url)
        list_page = ListPage(self).add_list_item('Get help')

        share_box = list_page.get_share_box()
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your@friend-email.com'
        )

        list_page.share_list_with(user_email_share)
        list_page.wait_for_check_email_in_list_share(user_email_share)

        self.browser = oni_browser
        MyListsPage(self).go_to_my_lists_page()

        self.browser.find_element(By.LINK_TEXT, 'Get help').click()

        self.wait_for(
            lambda: self.assertEqual(
                list_page.get_list_owner(),
                'edith@example.com'
            )
        )

        list_page.add_list_item('Hi Edith!')

        self.browser = edith_browser
        self.browser.refresh()
        list_page.wait_for_row_in_list_table('Hi Edith!')
    
    def test_error_message_if_user_with_provided_email_not_found(self):
        """
        Тест POST запрос с неправильным email`ом пользователя показывает ошибку
        на экран
        """
        self.create_pre_authenticated_session('edith@example.com')

        self.browser.get(self.live_server_url)
        list_page = ListPage(self).add_list_item('Get help')
        
        list_page.share_list_with('HAHHAHAHHAHAH@mail.com')
        self.wait_for(
            lambda: self.browser.find_element(
                By.CLASS_NAME, 'alert-warning'
            )
        )

        self.assertEqual(
            self.browser.find_element(By.CLASS_NAME, 'alert-warning').text,
            'Пользователь не найден!'
        )
