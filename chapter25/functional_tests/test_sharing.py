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
        self.create_pre_authenticated_session('oniciferous@example.com')
        
        self.browser = edith_browser
        self.browser.get(self.live_server_url)
        list_page = ListPage(self).add_list_item('Get help')

        share_box = list_page.get_share_box()
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.com'
        )

        list_page.share_list_with('oniciferous@example.com')

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
        list_page.wait_for_row_in_list_table('Hi Edith!', 2)