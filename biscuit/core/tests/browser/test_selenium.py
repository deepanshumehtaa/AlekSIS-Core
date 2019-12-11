import os

import pytest

from django.test.selenium import SeleniumTestCase, SeleniumTestCaseBase

SeleniumTestCaseBase.external_host = os.environ.get('TEST_HOST', '') or None
SeleniumTestCaseBase.browsers = list(filter(bool, os.environ.get('TEST_SELENIUM_BROWSERS', '').split(',')))
SeleniumTestCaseBase.selenium_hub = os.environ.get('TEST_SELENIUM_HUB', '') or None

class SeleniumTests(SeleniumTestCase):
    @classmethod
    def _screenshot(cls, filename):
        screenshot_path = os.environ.get('TEST_SCREENSHOT_PATH', None)
        if screenshot_path:
            os.makedirs(os.path.join(screenshot_path, cls.browser), exist_ok=True)
            return cls.selenium.save_screenshot(os.path.join(screenshot_path, cls.browser, filename))
        else:
            return False

    @pytest.mark.django_db
    def test_index(self):
        self.selenium.get(self.live_server_url + '/')
        assert 'BiscuIT' in self.selenium.title
        self._screenshot('index.png')
