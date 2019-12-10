import pytest

from django.test import LiveServerTestCase

webdriver = pytest.importorskip('selenium.webdriver')


class SeleniumTests(LiveServerTestCase):
    __test__ = False

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.selenium.set_window_size(1920, 1080)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_index(self):
        self.selenium.get(self.live_server_url + '/')
        assert 'BiscuIT' in self.selenium.title
        self.selenium.save_screenshot('screenshots/index.png')


class SeleniumTestsChromium(SeleniumTests):
    __test__ = True

    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-headless')
        options.add_argument('--disable-shm-usage')

        cls.selenium = webdriver.Chrome(options=options)

        super().setUpClass()
