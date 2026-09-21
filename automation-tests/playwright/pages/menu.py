from playwright.sync_api import Page


class MenuPage:
    def __init__(self, page: Page):
        root = page.locator('.menu')
        self.home = root.get_by_role('link', name='Home')
        self.cloth = root.get_by_role('link', name='Cloth')
        self.account = root.locator('a[href="/account"]')
        self.basket = root.locator('a[href="/basket"]')
        self.logout = root.locator('a[href="/logout"]')
        self.welcome = root.locator('.welcome-username')
