from playwright.sync_api import Page

from pages.menu import MenuPage


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.menu = MenuPage(page)
        self.username = page.locator('#login')
        self.password = page.locator('#password')
        self.submit = page.get_by_role('button', name='Submit')

    def open(self) -> None:
        self.page.goto('/login')

    def log_in(self, username: str, password: str) -> None:
        self.username.fill(username)
        self.password.fill(password)
        self.submit.click()
