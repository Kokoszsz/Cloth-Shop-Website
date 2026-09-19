@checkout
Feature: Check out my basket
  US-13
  As a shopper with clothes in my basket
  I want to fill in my delivery details at the checkout
  So that the shop knows where to send my clothes

  Scenario: Checkout needs something in the basket
    Given my basket is empty
    When I try to open the checkout
    Then I am taken to my basket instead

  @smoke
  Scenario: Go from the basket to the checkout
    Given I am not logged in
    And my basket has a product in it
    When I press "Order" on my basket page
    Then I see an empty checkout form

  Scenario: Logged-in customers get their details filled in
    # Jira CS-87
    Given I am logged in
    And my account has surname "Kowalski", phone "600100200", country "Poland" and city "Krakow"
    And my basket has a product in it
    When I open the checkout
    Then name, surname, country, city, phone and e-mail are filled in from my account

  Scenario: Home delivery asks for an address
    Given I am on the checkout with a product in my basket
    When I choose "Deliver to house"
    Then I am asked for city, address and post code
    And I am not asked for a parcel locker

  Scenario: Parcel locker delivery asks for a locker
    Given I am on the checkout with a product in my basket
    When I choose "Deliver to parcel locker"
    Then I am asked for a parcel locker
    And I am not asked for an address

  Scenario: Country suggestions for guests
    # Jira CS-64
    Given I am not logged in
    And I am on the checkout with a product in my basket
    When I type "Po" into the country field
    Then "Poland" is suggested
    When I pick "Poland"
    Then the country field says "Poland"

  Scenario: The terms must be accepted
    Given I am on the checkout with a product in my basket
    And I have filled in every field for home delivery
    When I press "Place Order" without accepting the terms
    Then I am asked to accept the terms
