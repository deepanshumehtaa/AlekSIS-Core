import sys

import pytest

if '--driver' not in sys.argv:
    pytest.skip('Selenium driver not configured', allow_module_level=True)

@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    return chrome_options

def test_index(selenium):
    selenium.get('http://app:8000/')
    assert 'BiscuIT' in selenium.title
    selenium.save_screenshot('screenshots/index.png')
