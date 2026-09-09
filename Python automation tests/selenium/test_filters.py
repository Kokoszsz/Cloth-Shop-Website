import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

pytestmark = pytest.mark.browser

CHECKBOX_IDS = {
    'male': 'maleCheckbox',
    'female': 'femaleCheckbox',
    't-shirt': 'tshirtCheckbox',
    'jeans': 'jeansCheckbox',
    'shirt': 'shirtCheckbox',
}


def displayed_product_names(driver):
    return [card.text for card in driver.find_elements(By.CSS_SELECTOR, '.product-item h2')]


def apply_filter(driver, wait, base_url, boxes, min_value, max_value):
    driver.get(f'{base_url}/cloth')
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.product-item')))
    before = len(displayed_product_names(driver))

    for box in boxes:
        driver.find_element(By.ID, CHECKBOX_IDS[box]).click()

    minimum = driver.find_element(By.ID, 'minValueInput')
    minimum.clear()
    minimum.send_keys(str(min_value))

    maximum = driver.find_element(By.ID, 'maxValueInput')
    maximum.clear()
    maximum.send_keys(str(max_value))

    driver.find_element(By.CSS_SELECTOR, 'input[name="filter_button"]').click()
    wait.until(lambda d: len(displayed_product_names(d)) != before)

    return displayed_product_names(driver)


@pytest.mark.parametrize(
    ('boxes', 'min_value', 'max_value', 'expected'),
    [
        pytest.param(
            ['male', 't-shirt'], 30, 70,
            {'Great T-shirt', 'Brown T-shirt', 'Red T-shirt', 'Red T-shirt Extra'},
            id='male-t-shirts-between-30-and-70',
        ),
        pytest.param(
            ['female', 'jeans'], 60, 100,
            {'Jeans Extra'},
            id='female-jeans-between-60-and-100',
        ),
        pytest.param(
            ['shirt'], 0, 0,
            {'Black Shirt', 'Pink Shirt'},
            id='shirts-at-any-price',
        ),
    ],
)
def test_the_filter_shows_only_matching_products(
    driver, wait, base_url, boxes, min_value, max_value, expected
):
    assert set(apply_filter(driver, wait, base_url, boxes, min_value, max_value)) == expected


def test_the_filter_excludes_products_outside_the_price_range(driver, wait, base_url):
    names = apply_filter(driver, wait, base_url, ['female', 'jeans'], 60, 100)

    assert 'Standard Jeans' not in names


def test_the_cloth_page_lists_every_product_before_filtering(driver, wait, base_url):
    driver.get(f'{base_url}/cloth')
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.product-item')))

    assert len(displayed_product_names(driver)) == 9
