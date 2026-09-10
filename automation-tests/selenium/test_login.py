import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

pytestmark = pytest.mark.browser


def test_login_shows_the_username_in_the_menu(driver, wait, credentials, log_in):
    log_in()

    welcome = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'welcome-username')))

    assert credentials['username'] in welcome.text
    assert driver.find_elements(By.CSS_SELECTOR, 'a[href="/logout"]')


def test_login_redirects_to_the_account_page(driver, wait, base_url, log_in):
    log_in()

    wait.until(EC.url_to_be(f'{base_url}/account'))

    assert driver.current_url == f'{base_url}/account'


def test_a_wrong_password_is_rejected(driver, wait, base_url, log_in):
    log_in(password='not-the-password')

    form = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'container')))

    assert 'Wrong Password' in form.text
    assert driver.current_url.rstrip('#') == f'{base_url}/login'
    assert not driver.find_elements(By.CLASS_NAME, 'welcome-username')


def test_an_unknown_username_is_rejected(driver, wait, base_url, log_in):
    log_in(username='no-such-user')

    form = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'container')))

    assert 'Wrong Username' in form.text
    assert not driver.find_elements(By.CLASS_NAME, 'welcome-username')


def test_the_account_page_requires_a_login(driver, wait, base_url):
    driver.get(f'{base_url}/account')

    wait.until(EC.url_to_be(f'{base_url}/login'))

    assert driver.find_element(By.ID, 'login').is_displayed()
