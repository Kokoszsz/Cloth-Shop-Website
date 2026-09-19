@auth
Feature: Log in
  US-01
  As a returning customer
  I want to log in with my username and password
  So that the shop recognises me and can reuse my saved details

  Background:
    Given I have a customer account
    And I am not logged in

  @smoke
  Scenario: Log in with the right username and password
    Given I am on the login page
    When I log in with my username and password
    Then I am taken to my account page
    And the menu greets me by my username
    And the menu offers a way to log out

  Scenario Outline: Wrong details are rejected without saying which one was wrong
    Given I am on the login page
    When I log in with <mistake>
    Then I see the error "Wrong username or password"
    And I am still not logged in

    Examples:
      | mistake                          |
      | my username and a wrong password |
      | a username nobody has            |

  Scenario: The account page sends guests to the login page
    When I open my account page
    Then I am taken to the login page

  Scenario: A logged-in customer is not shown the login page again
    Given I am logged in
    When I open the login page
    Then I am taken to the home page

  Scenario: Get from the login page to account creation
    Given I am on the login page
    When I choose "Create account"
    Then I am on the create account page
