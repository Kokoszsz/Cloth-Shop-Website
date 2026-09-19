@basket
Feature: Add clothes to my basket
  US-09
  As a shopper, with or without an account
  I want to put clothes in a basket while I browse
  So that I can buy them together at the end

  @smoke
  Scenario: Add a product from the catalogue
    Given I am on the Cloth page
    When I add "Great T-shirt" to the basket
    Then I see the message "Product added to basket successfully!"
    When I close the message
    Then the message is gone
    And my basket contains "Great T-shirt"
    And the basket total is "34.00 $"

  Scenario: Add a product from its product page
    Given I am on a product page
    When I add it to the basket
    Then I see the message "Product added to basket successfully!"
    And my basket contains that product

  Scenario: Add a product from a filtered catalogue
    Given I am on the Cloth page
    And I have filtered by Woman
    When I add one of the filtered products to the basket
    Then my basket contains that product

  Scenario: The total adds up several products
    Given I have added "Great T-shirt" and "Black Shirt" to the basket
    When I open my basket
    Then the basket total is "90.99 $"

  Scenario: The basket survives browsing around
    Given I have added a product to the basket
    When I visit the home page and the Cloth page
    And I open my basket
    Then my basket still contains that product

  Scenario: An empty basket
    Given I have not added anything
    When I open my basket
    Then the basket shows no products
    And the basket total is "0.00 $"

  Scenario: Change how many of a product I want
    Given I have added "Great T-shirt" to the basket
    When I change its quantity to 2
    Then the basket total is "68.00 $"
    And the quantity is still 2 after reloading the page
