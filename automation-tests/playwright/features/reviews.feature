@reviews
Feature: Review clothes
  US-12
  As a logged-in customer
  I want to write a short review of a piece of clothing
  So that I can tell other shoppers what the stars cannot

  Scenario: Guests cannot write reviews
    Given I am not logged in
    When I open a product page
    Then I do not see the review box

  @smoke
  Scenario: Post a review
    Given I am logged in
    And I am on a product page
    When I post the review "Nice fabric, fits well."
    And I reload the page
    Then I see my review "Nice fabric, fits well." under my username
    And my review has a Remove button

  Scenario: A new review shows my name straight away
    Given I am logged in
    And I am on a product page
    When I post the review "Nice fabric, fits well."
    Then my review shows my username and today's date without reloading

  Scenario Outline: A review must be 5 to 1000 characters
    Given I am logged in
    And I am on a product page
    When I post a review that is <length> characters long
    Then I see the error "<message>"
    And no review is added

    Examples:
      | length | message                                      |
      | 4      | Review is too short (minimum 5 characters)   |
      | 1001   | Review is too long (maximum 1000 characters) |

  Scenario: Only one review per product
    Given I am logged in
    And I have already reviewed a product
    When I post another review of it
    Then I see the error "You have already reviewed this product"

  Scenario: Remove my own review
    Given I am logged in
    And I have reviewed a product
    When I remove my review
    And I reload the page
    Then my review is gone

  Scenario: I cannot remove someone else's review
    Given another customer has reviewed a product
    And I am logged in
    When I open that product's page
    Then their review has no Remove button

  @security
  Scenario: Review text is shown as plain text, never run as code
    Given I am logged in
    And I am on a product page
    When I post the review "<b>bold</b> and <script>window.hacked = 1</script>"
    And I reload the page
    Then I see the review text exactly as I typed it
    And no script from the review has run
