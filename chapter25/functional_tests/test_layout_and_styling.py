from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest
from .list_page import ListPage


class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # Edith goes to the home page,
        self.browser.get(self.live_server_url)

        # Her browser window is set to a very specific size
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        list_page = ListPage(self).assert_size_almost_equal()

        # She starts a new list and sees the input is nicely
        # centered there too
        list_page.start_a_new_list('testing')

        list_page.assert_size_almost_equal()