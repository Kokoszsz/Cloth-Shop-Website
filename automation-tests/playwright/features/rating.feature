@rating
Feature: Rate clothes
  US-11
  As a logged-in customer
  I want to give a piece of clothing 1 to 5 stars
  So that other shoppers can see what people think of it

  Scenario: Guests see the rating but cannot rate
    Given I am not logged in
    When I open a product page
    Then I see the product's total rating
    But I do not see the stars or the reset button

  @smoke
  Scenario: Rate a product
    Given I am logged in
    And I am on the page of a product nobody has rated yet
    When I give it 4 stars
    And I reload the page
    Then 4 stars are still selected
    And the total rating shows 4

  Scenario: My stars are averaged with other customers' stars
    Given another customer gave a product 3 stars
    And I am logged in
    And I am on that product's page
    When I give it 5 stars
    And I reload the page
    Then the total rating shows 4

  Scenario: Changing my mind replaces my rating
    Given I am logged in
    And I gave 2 stars to a product nobody else has rated
    When I give it 5 stars instead
    And I reload the page
    Then 5 stars are selected
    And the total rating shows 5

  Scenario: Reset my rating
    Given I am logged in
    And I gave 4 stars to a product nobody else has rated
    When I press "Reset Rating"
    And I reload the page
    Then no stars are selected
    And the total rating shows 0
