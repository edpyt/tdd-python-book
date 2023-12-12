import time
from typing import Callable, Optional, Sequence

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import wait


class ListPage:
    def __init__(self, test) -> None:
        self.test = test
    
    def get_table_rows(self):
        return self.test.browser.find_elements(
            By.CSS_SELECTOR, '#id_list_table tr'
        )

    @wait
    def wait_for_row_in_list_table(self, row_text):
        rows = self.get_table_rows()
        try:
            self.test.assertIn(row_text, [row.text for row in rows])
        except:
            if hasattr(self.test, 'get_error_element'):
                self.test.assertEqual(
                    self.test.get_error_element().text,
                    "You've already got this in your list"
                )
    
    def get_item_input_box(self):
        return self.test.browser.find_element(By.ID, 'id_text')
    
    def add_list_item(self, item_text):
        new_item_no = len(self.get_table_rows()) +  1
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table(f'{new_item_no}: {item_text}')
        return self
    
    def assert_size_almost_equal(self):
        inputbox = self.get_item_input_box()
        self.test.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2,
            270,
            delta=10,
        )
        return self

    def get_share_box(self):
        return self.test.wait_for(
            lambda: self.test.browser.find_element(
                By.NAME, 'sharee'
            )
        )
    
    def wait_for_check_email_in_list_share(self, email: str):
        self.test.wait_for(
            lambda: self.test.assertIn(
                email,
                [item.text for item in self.get_shared_with_list()]
            )
        )

    def get_shared_with_list(self):
        return self.test.browser.find_element(
            By.CSS_SELECTOR, '.list-sharee'
        ).find_elements(By.TAG_NAME, 'li')
    
    def send_keys_and_wait_for(
        self,
        send_key: str | list[str],
        *wait_fors: Sequence[Callable],
        web_element: Optional[WebElement] =None
    ):
        if not web_element:
            web_element = self.get_item_input_box()

        if isinstance(send_key, list):
            web_element.send_keys(*send_key)
        else:
            web_element.send_keys(send_key)

        if wait_fors:
            for wait_for in wait_fors:
                self.test.wait_for(wait_for)
        return self
    
    def click_and_wait_for(
        self,
        web_element: WebElement,
        *wait_fors: Sequence[Callable]
    ):
        web_element.click()
        if wait_fors:
            for wait_for in wait_fors:
                self.test.wait_for(wait_for)
        return self

    def share_list_with(self, email):
        self.get_share_box().send_keys(email)
        self.get_share_box().send_keys(Keys.ENTER)

    
    def start_a_new_list(self, item_text):
        inputbox = self.get_item_input_box()
        inputbox.send_keys(item_text)
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table(item_text)
        return self
    
    def get_list_owner(self):
        return self.test.browser.find_element(By.ID, 'id_list_owner').text