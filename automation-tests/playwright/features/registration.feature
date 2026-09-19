@auth
Feature: Create an account
  US-03
  As a new visitor
  I want to create an account with a username, e-mail and password
  So that I can rate and review clothes and have my details filled in at checkout

  Background:
    Given I am not logged in
    And I am on the create account page

  @smoke
  Scenario: Create an account with valid details
    When I register with a new username, a new e-mail and the password "longpass1"
    Then I am taken to my account page
    And the menu greets me by my new username
    And my account page shows the username and e-mail I registered with

  Scenario: The new account works for logging in later
    Given I have registered with the password "longpass1"
    And I have logged out
    When I log in with that username and "longpass1"
    Then the menu greets me by my new username

  Scenario Outline: Invalid details are rejected with a message
    When I register with username "<username>", e-mail "<email>" and password "<password>"
    Then I see the error "<message>"
    And I am still not logged in

    Examples:
      | username | email          | password   | message                                        |
      |          | a@shop.test    | longpass1  | No Username provided                           |
      | john doe | b@shop.test    | longpass1  | Username can not have spaces                   |
      | newuser1 |                | longpass1  | No E-mail provided                             |
      | newuser2 | c@shop.test    | short      | Password must consist of at least 8 characters |
      | newuser3 | d@shop.test    | long pass1 | Password can not have spaces                   |

  Scenario: The username is already taken
    Given another customer already uses the username "taken-name"
    When I register with username "taken-name", a new e-mail and the password "longpass1"
    Then I see the error "Already such an User"

  Scenario: The e-mail is already used
    Given another customer already uses the e-mail "taken@shop.test"
    When I register with a new username, e-mail "taken@shop.test" and the password "longpass1"
    Then I see the error "Already such an E-mail"
