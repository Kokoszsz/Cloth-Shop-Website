from data import PRICE_IN_DOLLARS
from pages.catalogue_page import CataloguePage
from pages.menu import MenuPage
from playwright.sync_api import Page, expect
from pytest_bdd import parsers, scenarios, then, when

scenarios('../features/catalogue.feature')


@when('I open the shop')
def open_shop(page: Page):
    page.goto('/')


@when('I open the Cloth page from the menu')
def open_cloth_page(page: Page, menu_page: MenuPage):
    page.goto('/')
    menu_page.cloth.click()


@then('I see "Welcome to Kokosz Cloth Shop"')
def see_welcome_message(page: Page):
    expect(page.locator('text=Welcome to Kokosz Cloth Shop')).to_be_visible()


@then('the menu links to Home, Cloth, my account and my basket')
def see_main_menu(menu_page: MenuPage):
    expect(menu_page.home).to_be_visible()
    expect(menu_page.cloth).to_be_visible()
    expect(menu_page.account).to_be_visible()
    expect(menu_page.basket).to_be_visible()


@then(parsers.re(r'I see (?P<count>\d+) products'))
def see_products(catalogue_page: CataloguePage, count: str):
    expect(catalogue_page.products).to_have_count(int(count))


@then('every product shows a name, a picture and a price in dollars')
def see_product_details(catalogue_page: CataloguePage):
    shown = catalogue_page.products.count()
    expect(catalogue_page.names).to_have_count(shown)
    expect(catalogue_page.pictures).to_have_count(shown)
    expect(catalogue_page.prices).to_have_count(shown)
    for price in catalogue_page.prices.all_inner_texts():
        assert PRICE_IN_DOLLARS.fullmatch(price), price
