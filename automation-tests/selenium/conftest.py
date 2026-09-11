import os
import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_BASE_URL = 'http://localhost:5000'
DEFAULT_TIMEOUT = 10
POLL_INTERVAL = 0.25


def pytest_addoption(parser):
    parser.addoption(
        '--selenium-headed',
        action='store_true',
        default=False,
        help='run the browser with a visible window instead of headless',
    )
    parser.addoption(
        '--shop-url',
        action='store',
        default=os.environ.get('SHOP_BASE_URL', DEFAULT_BASE_URL),
        help=f'base URL of the running shop (default {DEFAULT_BASE_URL})',
    )


@pytest.fixture(scope='session')
def base_url(request):
    return request.config.getoption('--shop-url').rstrip('/')


@pytest.fixture
def driver(request):
    options = Options()
    if not request.config.getoption('--selenium-headed'):
        options.add_argument('-headless')

    driver = webdriver.Firefox(options=options)
    driver.set_window_size(1280, 1024)
    try:
        yield driver
    finally:
        driver.quit()


@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, DEFAULT_TIMEOUT)


@pytest.fixture
def credentials():
    return {'username': 'test', 'password': '123'}


@pytest.fixture
def log_in(driver, wait, base_url, credentials):
    def _log_in(username=None, password=None):
        driver.get(f'{base_url}/login')
        login_field = wait.until(EC.visibility_of_element_located((By.ID, 'login')))
        login_field.send_keys(credentials['username'] if username is None else username)
        password_field = driver.find_element(By.ID, 'password')
        password_field.send_keys(credentials['password'] if password is None else password)
        driver.find_element(By.CSS_SELECTOR, 'input.submit').click()

    return _log_in


@pytest.fixture
def basket_contents(driver, base_url):
    def _basket_contents(until=None, timeout=DEFAULT_TIMEOUT):
        deadline = time.monotonic() + timeout
        while True:
            driver.get(f'{base_url}/basket')
            names = [item.text for item in driver.find_elements(By.CSS_SELECTOR, '.basket-item h3')]
            if until is None or names == until or time.monotonic() > deadline:
                return names
            time.sleep(POLL_INTERVAL)

    return _basket_contents
