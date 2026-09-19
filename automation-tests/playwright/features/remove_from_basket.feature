@basket
Feature: Remove clothes from my basket
  US-10
  As a shopper
  I want to take clothes back out of my basket
  So that I only order what I really want

  Background:
    Given I have added "Great T-shirt" and "Black Shirt" to the basket
    And I am on my basket page

  Scenario: The removed product is gone after reloading
    When I remove "Great T-shirt"
    And I reload the page
    Then my basket contains only "Black Shirt"
    And the basket total is "56.99 $"

  Scenario: The removed product disappears straight away
    When I remove "Great T-shirt"
    Then "Great T-shirt" disappears without reloading the page
    And the basket total changes to "56.99 $"

  Scenario: A product added twice and removed once
    Given I have added "Great T-shirt" to the basket a second time
    When I remove "Great T-shirt"
    And I reload the page
    Then my basket does not contain "Great T-shirt"
