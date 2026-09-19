@catalogue
Feature: Browse the clothes
  US-06
  As a shopper
  I want to see every piece of clothing with its picture and price
  So that I can find something I like

  US-07
  As a shopper
  I want to open a page for one piece of clothing
  So that I can look at it closely before buying

  @smoke
  Scenario: The home page opens with the menu
    When I open the shop
    Then I see "Welcome to Kokosz Cloth Shop"
    And the menu links to Home, Cloth, my account and my basket

  @smoke
  Scenario: The catalogue lists every product
    When I open the Cloth page from the menu
    Then I see 9 products
    And every product shows a name, a picture and a price in dollars

  Scenario: Open a product page from the catalogue
    Given I am on the Cloth page
    When I open "Red T-shirt"
    Then I see the product page for "Red T-shirt" priced "37.00 $"

  Scenario: Open a product page after filtering
    Given I am on the Cloth page
    And I have filtered by Woman
    When I open "Pink Shirt"
    Then I see the product page for "Pink Shirt"

  Scenario Outline: A product that does not exist
    Given I am <visitor>
    When I open the product page for "no-such-product"
    Then I see "Product Not Found"
    And I can go back to the clothes

    Examples:
      | visitor       |
      | not logged in |
      | logged in     |
