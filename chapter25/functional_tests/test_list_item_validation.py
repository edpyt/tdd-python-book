import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


from .base import FunctionalTest
from .list_page import ListPage


class ItemValidationTest(FunctionalTest):
    def get_error_element(self):
        return self.browser.find_element(By.CSS_SELECTOR, '.has-error')

    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.live_server_url)
        
        list_page = ListPage(self).send_keys_and_wait_for(
            Keys.ENTER,
            lambda: self.browser.find_element(
                By.CSS_SELECTOR, '#id_text:invalid'
            )
        )

        list_page.send_keys_and_wait_for(
            'Buy milk',
            lambda: (
                self.browser.find_element(By.CSS_SELECTOR, '#id_text:valid')
            )
        )

        list_page.send_keys_and_wait_for(
            Keys.ENTER,
            lambda: self.wait_for_row_in_list_table('1: Buy milk')
        )

        list_page.send_keys_and_wait_for(
            Keys.ENTER,
            lambda: self.wait_for_row_in_list_table('1: Buy milk'),
            lambda: self.browser.find_element(
                By.CSS_SELECTOR, '#id_text:invalid'
            )
        )

        list_page.send_keys_and_wait_for(
            Keys.ENTER,
            lambda: self.wait_for_row_in_list_table('1: Buy milk')
        )

        list_page.send_keys_and_wait_for(
            'Make tea',
            lambda: self.browser.find_element(
                By.CSS_SELECTOR, '#id_text:valid'
            )
        )

        list_page.send_keys_and_wait_for(
            Keys.ENTER,
            lambda: self.wait_for_row_in_list_table('1: Buy milk'),
            lambda: self.wait_for_row_in_list_table('2: Make tea')
        )


    def test_cannot_add_duplicate_items(self):
        self.browser.get(self.live_server_url)
        ListPage(self).add_list_item('Buy wellies')
    
    def test_error_messages_are_cleared_on_input(self):
        self.browser.get(self.live_server_url)

        list_page = ListPage(self).add_list_item('Banter too thick')
        list_page.add_list_item('Banter too thick')

        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))

        list_page.send_keys_and_wait_for(
            'a', 
            lambda: self.assertFalse(self.get_error_element().is_displayed())
        )
