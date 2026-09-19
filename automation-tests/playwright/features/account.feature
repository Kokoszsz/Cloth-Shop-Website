@account
Feature: Manage my account details
  US-04
  As a logged-in customer
  I want to keep my contact and delivery details up to date
  So that they are filled in for me when I check out

  US-05
  As a logged-in customer
  I want to change my password
  So that I can keep my account safe

  Background:
    Given I am logged in
    And I am on my account page

  Scenario: Save my details
    When I change my username to a new one
    And I set my surname to "Kowalski", phone to "600100200", country to "Poland" and city to "Krakow"
    And I save my changes
    And I log out and log in again with my new username and my old password
    Then the menu greets me by my new username
    And my account page shows surname "Kowalski", phone "600100200", country "Poland" and city "Krakow"

  Scenario: Change my password
    When I enter the new password "newpass123"
    And I save my changes
    And I log out
    Then I cannot log in with my old password
    But I can log in with "newpass123"
