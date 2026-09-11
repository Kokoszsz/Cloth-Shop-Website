from playwright.sync_api import Page, expect


def test_filter_and_add_to_basket(page: Page):
    # Navigate to the website
    page.goto("http://127.0.0.1:5000/")

    # Verify that we're on the homepage
    expect(page).to_have_title("Kokosz Cloth Shop")

    # Click on the Cloth link in navigation
    page.get_by_role("link", name="Cloth").click()

    # Verify that we're on the cloth page
    expect(page).to_have_title("Kokosz Cloth Shop Cloth")

    # Check the "Man" filter option using ID selector
    page.locator("#maleCheckbox").check()

    # Click the Filter button
    page.get_by_role("button", name="Filter").click()

    # Add the first product (Great T-shirt) to the basket
    # Find the first product's add to basket button using its class and click it
    page.locator(".add-to-basket").first.click()

    # Verify that the product was added successfully
    success_message = page.locator("text=Product added to basket successfully!")
    expect(success_message).to_be_visible()

    # Click the OK button to dismiss the success message
    page.get_by_role("link", name="OK").click()

    # Verify that the success message is no longer visible
    expect(success_message).not_to_be_visible()
