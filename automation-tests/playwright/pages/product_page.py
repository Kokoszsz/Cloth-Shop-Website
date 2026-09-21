from playwright.sync_api import Page

from pages.menu import MenuPage


class ProductPage:
    def __init__(self, page: Page):
        self.page = page
        self.menu = MenuPage(page)

    def open(self, slug: str) -> None:
        self.page.goto(f'/cloth/product_detail/{slug}')
