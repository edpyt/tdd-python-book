import time
import os
from typing import Any, Callable

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from functional_tests.server_tools import reset_database

MAX_WAIT = 10


def wait(fn: Callable) -> Callable:
    def modified_fn(instance: object, find_element: str) -> Any:
        start_time = time.time()

        while True:
            try:
                return fn(instance, find_element)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.staging_server = os.environ.get('STAGING_SERVER')
        if self.staging_server:
            self.live_server_url = 'http://' + self.staging_server
            reset_database()

    def tearDown(self):
        self.browser.quit()
    

    def get_item_input_box(self):
        return self.browser.find_element(By.ID, 'id_text')

    @wait
    def wait_for(self, fn: Callable) -> Any:
        return fn()
    
    @wait
    def wait_for_row_in_list_table(self, row_text):
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(row_text, [row.text for row in rows])

    @wait
    def wait_to_be_logged_in(self, email: str):
        self.browser.find_element(By.LINK_TEXT, 'Log out')
        navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email: str):
        self.browser.find_element(By.NAME, 'email')
        navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertNotIn(email, navbar.text)
