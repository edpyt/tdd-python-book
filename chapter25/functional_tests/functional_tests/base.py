from datetime import datetime
import time
import os
from typing import Any, Callable

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from functional_tests.server_tools import (
    create_session_on_server, reset_database
)
from .management.commands.create_session import (
    create_pre_authenticated_session
)

MAX_WAIT = 10

SCREEN_DUMP_LOCATION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'screendumps'
)


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
        if self._test_has_failed() and os.environ.get('STAGING_SERVER'):
            if not os.path.exists(SCREEN_DUMP_LOCATION):
                os.makedirs(SCREEN_DUMP_LOCATION)
            for ix, handle in enumerate(self.browser.window_handles):
                self._windowid = ix
                self.browser.switch_to.window(handle)
                self.take_screenshot()
                self.dump_html()
        self.browser.quit()
        super().tearDown()

    def _test_has_failed(self):
        errors = self._outcome.result.errors + self._outcome.result.failures
        return any(error for (method, error) in errors)

    def create_pre_authenticated_session(self, email: str):
        if self.staging_server:
            session_key = create_session_on_server(email)
        else:
            session_key = create_pre_authenticated_session(email)

        self.browser.get(self.live_server_url + '/404_no_such_url/')
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/'
        ))

    def take_screenshot(self):
        filename = self._get_filename() + '.png'
        print('screenshotting to', filename)
        self.browser.get_screenshot_as_file(filename)

    def dump_html(self):
        filename = self._get_filename() + '.html'
        print('dumping page HTML to', filename)
        with open(filename, 'w') as f:
            f.write(self.browser.page_source)

    def _get_filename(self):
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        return (
            f'{SCREEN_DUMP_LOCATION}/'
            f'{self.__class__.__name__}.'
            f'{self._testMethodName}-window'
            f'{self._windowid}-'
            f'{timestamp}'   
        )

    def add_list_item(self, item_text):
        num_rows = len(
            self.browser.find_elements(By.CSS_SELECTOR, '#id_list_table tr')
        )
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        item_number = num_rows + 1
        self.wait_for_row_in_list_table(f'{item_number}: {item_text}')

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
