@auth
Feature: Log out
  US-02
  As a customer on a shared computer
  I want to log out
  So that the next person cannot act as me or see my basket

  Background:
    Given I am logged in

  @smoke
  Scenario: Log out from the menu
    When I log out
    Then I am on the home page
    And the menu no longer greets me
    And the menu no longer offers a way to log out

  Scenario: Logging out empties the basket
    Given my basket has a product in it
    When I log out
    Then my basket is empty

  Scenario: The account page is protected again after logging out
    When I log out
    And I open my account page
    Then I am taken to the login page
