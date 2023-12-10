import os
import re
import poplib
import time
from typing import Optional

from django.core import mail
from django.conf import settings
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):
    def setUp(self):
        super().setUp()

        if self.staging_server:
            self.TEST_EMAIL = settings.EMAIL_HOST_USER
        else:
            self.TEST_EMAIL = 'edith@example.com'

    def test_can_get_email_link_to_log_in(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.NAME, 'email').send_keys(self.TEST_EMAIL)
        self.browser.find_element(By.NAME, 'email').send_keys(Keys.ENTER)

        self.wait_for(
            lambda: self.assertIn(
                'Проверьте свою почту',
                self.browser.find_element(By.TAG_NAME, 'body').text
            )
        )

        body = self.wait_for_email(self.TEST_EMAIL, SUBJECT)

        self.assertIn('Use this link to log in', body)
        url_search = re.search(r'http://.+/.+$', body)
        assert url_search, 'Could not find url in email body'
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        self.browser.get(url)

        self.wait_for(
            lambda: self.browser.find_element(By.LINK_TEXT, 'Log out')
        )
        navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertIn(self.TEST_EMAIL, navbar.text)

        # Вход в систему...
        self.wait_to_be_logged_in(self.TEST_EMAIL)
        
        # Пользователь выходит из системы...
        self.browser.find_element(By.LINK_TEXT, 'Log out').click()

        # Выход из системы...
        self.wait_to_be_logged_out(self.TEST_EMAIL)

    def wait_for_email(self, test_email: str, subject: str) -> Optional[str]:
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body
        
        email_id: Optional[int] = None
        start = time.time()
        inbox = poplib.POP3_SSL('pop.mail.ru')
        try:
            inbox.user(test_email)
            inbox.pass_(settings.EMAIL_HOST_PASSWORD)
            while time.time() - start < 60:
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print('getting msg', i)
                    _, lines, __ = inbox.retr(i)
                    lines = [l.decode('utf8') for l in lines]
                    if any(subject.lower() in param.lower() for param in lines):
                        email_id = i
                        body = '\n'.join(lines)
                        return body
                time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id) 
            inbox.quit()