import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

pytestmark = pytest.mark.browser

ADDED_MESSAGE = 'Product added to basket successfully!'


def add_first_products(driver, wait, base_url, count):
    driver.get(f'{base_url}/cloth')
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.product-item')))

    added = []
    for index in range(count):
        card = driver.find_elements(By.CSS_SELECTOR, '.product-item')[index]
        added.append(card.find_element(By.CSS_SELECTOR, 'h2').text)
        card.find_element(By.CSS_SELECTOR, '.add-to-basket').click()

        modal = wait.until(EC.visibility_of_element_located((By.ID, 'myModal')))
        modal.find_element(By.LINK_TEXT, 'OK').click()
        wait.until(EC.invisibility_of_element_located((By.ID, 'myModal')))

    return added


def test_adding_a_product_shows_the_confirmation_message(driver, wait, base_url):
    driver.get(f'{base_url}/cloth')
    card = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.product-item')))

    card.find_element(By.CSS_SELECTOR, '.add-to-basket').click()

    modal = wait.until(EC.visibility_of_element_located((By.ID, 'myModal')))

    assert ADDED_MESSAGE in modal.text


def test_the_confirmation_message_closes_on_ok(driver, wait, base_url):
    driver.get(f'{base_url}/cloth')
    card = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.product-item')))
    card.find_element(By.CSS_SELECTOR, '.add-to-basket').click()
    modal = wait.until(EC.visibility_of_element_located((By.ID, 'myModal')))

    modal.find_element(By.LINK_TEXT, 'OK').click()

    wait.until(EC.invisibility_of_element_located((By.ID, 'myModal')))

    assert not driver.find_element(By.ID, 'myModal').is_displayed()


def test_the_added_product_appears_in_the_basket(driver, wait, base_url, basket_contents):
    added = add_first_products(driver, wait, base_url, 1)

    assert basket_contents(until=added) == added


def test_the_basket_keeps_every_added_product(driver, wait, base_url, basket_contents):
    added = add_first_products(driver, wait, base_url, 3)

    assert basket_contents(until=added) == added


def test_the_basket_is_empty_before_anything_is_added(driver, base_url, basket_contents):
    assert basket_contents() == []
