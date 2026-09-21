from playwright.sync_api import Page

from pages.menu import MenuPage


class BasketPage:
    def __init__(self, page: Page):
        self.page = page
        self.menu = MenuPage(page)

    def open(self) -> None:
        self.page.goto('/basket')
