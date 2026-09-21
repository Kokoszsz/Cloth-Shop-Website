from playwright.sync_api import Page

from pages.menu import MenuPage


class CataloguePage:
    def __init__(self, page: Page):
        self.page = page
        self.menu = MenuPage(page)
        self.products = page.locator('.product-item')
        self.names = page.locator('#product-grid h2')
        self.pictures = page.locator('#product-grid img')
        self.prices = page.locator('#product-grid .price')

    def open(self) -> None:
        self.page.goto('/cloth')
