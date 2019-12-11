import os

import pytest

from django.test.selenium import SeleniumTestCase


if not os.environ.get('TEST_SELENIUM_HUB', None):
    pytest.skip('Selenium hub not defined.', allow_module_level=True)


class SeleniumTests(SeleniumTestCase):
    external_host = os.environ.get('TEST_LISTEN_ADDRESS', '127.0.0.1')
    browsers = ['chrome', 'firefox']
    selenium_hub = 'http://%s/wd/hub' % os.environ.get('TEST_SELENIUM_HUB', '127.0.0.1:4444')

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
