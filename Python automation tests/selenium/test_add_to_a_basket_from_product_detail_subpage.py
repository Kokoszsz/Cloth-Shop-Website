import pytest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

pytestmark = pytest.mark.browser

ADDED_MESSAGE = 'Product added to basket successfully!'


def open_first_product_detail(driver, wait, base_url):
    driver.get(f'{base_url}/cloth')
    card = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.product-item')))
    name = card.find_element(By.CSS_SELECTOR, 'h2').text
    card.find_element(By.CSS_SELECTOR, '.product-link').click()
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'product-name')))
    return name


def add_to_basket(driver, wait):
    details = driver.find_element(By.CLASS_NAME, 'product-details')
    ActionChains(driver).move_to_element(details).perform()
    wait.until(EC.invisibility_of_element_located((By.ID, 'myresult')))
    driver.find_element(By.CSS_SELECTOR, '.add-to-basket').click()
    return wait.until(EC.visibility_of_element_located((By.ID, 'myModal')))


def test_the_detail_page_shows_the_product_from_the_card(driver, wait, base_url):
    name = open_first_product_detail(driver, wait, base_url)

    assert driver.find_element(By.CLASS_NAME, 'product-name').text == name


def test_the_detail_page_url_matches_the_product(driver, wait, base_url):
    name = open_first_product_detail(driver, wait, base_url)

    assert driver.current_url.startswith(f'{base_url}/cloth/product_detail/')
    assert name.replace(' ', '-') in driver.current_url


def test_adding_from_the_detail_page_shows_the_confirmation_message(driver, wait, base_url):
    open_first_product_detail(driver, wait, base_url)

    modal = add_to_basket(driver, wait)

    assert ADDED_MESSAGE in modal.text


def test_adding_from_the_detail_page_fills_the_basket(driver, wait, base_url, basket_contents):
    name = open_first_product_detail(driver, wait, base_url)

    modal = add_to_basket(driver, wait)
    modal.find_element(By.LINK_TEXT, 'OK').click()
    wait.until(EC.invisibility_of_element_located((By.ID, 'myModal')))

    assert basket_contents(until=[name]) == [name]
