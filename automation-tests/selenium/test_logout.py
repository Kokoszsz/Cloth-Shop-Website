import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

pytestmark = pytest.mark.browser


def test_logout_removes_the_username_from_the_menu(driver, wait, log_in):
    log_in()
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'welcome-username')))

    driver.find_element(By.CSS_SELECTOR, 'a[href="/logout"]').click()

    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'welcome-username')))

    assert not driver.find_elements(By.CLASS_NAME, 'welcome-username')
    assert not driver.find_elements(By.CSS_SELECTOR, 'a[href="/logout"]')


def test_logout_returns_to_the_home_page(driver, wait, base_url, log_in):
    log_in()
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'welcome-username')))

    driver.find_element(By.CSS_SELECTOR, 'a[href="/logout"]').click()

    wait.until(EC.url_to_be(f'{base_url}/'))

    assert driver.title == 'Kokosz Cloth Shop'


def test_the_account_page_is_protected_again_after_logout(driver, wait, base_url, log_in):
    log_in()
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'welcome-username')))
    driver.find_element(By.CSS_SELECTOR, 'a[href="/logout"]').click()
    wait.until(EC.url_to_be(f'{base_url}/'))

    driver.get(f'{base_url}/account')

    wait.until(EC.url_to_be(f'{base_url}/login'))

    assert driver.find_element(By.ID, 'login').is_displayed()
