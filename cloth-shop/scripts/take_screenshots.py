"""Drive a running shop with Playwright and save the screenshots used in the READMEs."""
import argparse
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = REPO_ROOT / 'docs' / 'screenshots'
DEFAULT_BASE_URL = 'http://127.0.0.1:5000'
VIEWPORT = {'width': 1280, 'height': 800}
USERNAME = 'test'
PASSWORD = '123'
PRODUCT_SLUG = 'Great-T-shirt'
REVIEW = 'Fits well and the fabric is heavier than I expected. Would buy again.'


IMAGES_LOADED = (
    'Array.from(document.images)'
    '.every(image => image.complete && image.naturalWidth > 0)'
)
FADE_FINISHED = (
    "Array.from(document.querySelectorAll('#fade-container > *'))"
    ".every(element => getComputedStyle(element).opacity === '1')"
)


def settle(page: Page) -> None:
    page.wait_for_load_state('networkidle')
    page.wait_for_function(IMAGES_LOADED)


def save(page: Page, output: Path, name: str, full_page: bool = False) -> None:
    settle(page)
    page.screenshot(path=str(output / f'{name}.png'), full_page=full_page)
    print(f'  {name}.png')


def log_in(page: Page, base_url: str) -> None:
    page.goto(f'{base_url}/login')
    page.fill('#login', USERNAME)
    page.fill('#password', PASSWORD)
    page.click('input.submit')
    page.wait_for_url(f'{base_url}/account')


def add_product_to_basket(page: Page, position: int) -> None:
    page.locator('.add-to-basket').nth(position).click()
    page.get_by_role('link', name='OK').click()


def capture(page: Page, base_url: str, output: Path) -> None:
    page.goto(f'{base_url}/')
    page.wait_for_function(FADE_FINISHED, timeout=30000)
    save(page, output, 'home')

    page.goto(f'{base_url}/cloth')
    page.locator('#maleCheckbox').check()
    page.get_by_role('button', name='Filter').click()
    save(page, output, 'catalogue')

    log_in(page, base_url)

    page.goto(f'{base_url}/cloth/product_detail/{PRODUCT_SLUG}')
    page.locator('label[for="star4"]').click()
    page.fill('#reviewText', REVIEW)
    page.click('#reviewButton')
    page.wait_for_timeout(500)
    page.goto(f'{base_url}/cloth/product_detail/{PRODUCT_SLUG}')
    save(page, output, 'product-detail', full_page=True)

    page.goto(f'{base_url}/cloth')
    add_product_to_basket(page, 0)
    add_product_to_basket(page, 2)
    page.goto(f'{base_url}/basket')
    save(page, output, 'basket')

    page.goto(f'{base_url}/checkout')
    save(page, output, 'checkout')

    page.goto(f'{base_url}/api/docs')
    page.wait_for_selector('.swagger-ui .opblock', timeout=15000)
    save(page, output, 'api-docs')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', default=DEFAULT_BASE_URL)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    arguments = parser.parse_args()

    arguments.output.mkdir(parents=True, exist_ok=True)
    print(f'Shooting {arguments.base_url} into {arguments.output}')

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport=VIEWPORT)
        try:
            capture(page, arguments.base_url.rstrip('/'), arguments.output)
        finally:
            browser.close()


if __name__ == '__main__':
    main()
