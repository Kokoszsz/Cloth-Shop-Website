@catalogue
Feature: Filter the clothes
  US-08
  As a shopper
  I want to narrow the catalogue by gender, type of clothing and price
  So that I only see clothes I would actually buy

  Background:
    Given I am on the Cloth page

  Scenario Outline: Filter by gender and type
    When I tick <filters>
    And I press Filter
    Then I see exactly these products: <products>

    Examples:
      | filters           | products                                                                              |
      | Man               | Great T-shirt, Brown T-shirt, Red T-shirt, Red T-shirt Extra, Male Jeans              |
      | Woman             | Black Shirt, Pink Shirt, Standard Jeans, Jeans Extra                                  |
      | Jeans             | Standard Jeans, Jeans Extra, Male Jeans                                               |
      | Woman and Jeans   | Standard Jeans, Jeans Extra                                                           |
      | T-shirt and Shirt | Great T-shirt, Brown T-shirt, Red T-shirt, Red T-shirt Extra, Black Shirt, Pink Shirt |

  @smoke
  Scenario: Filter by a price range
    When I set the price from 40 to 60
    And I press Filter
    Then I see exactly these products: Black Shirt, Pink Shirt, Standard Jeans, Male Jeans, Brown T-shirt

  Scenario: A price exactly on a limit counts as inside the range
    When I set the price from 34 to 54
    And I press Filter
    Then I see exactly these products: Great T-shirt, Red T-shirt, Pink Shirt, Brown T-shirt

  Scenario: Only a minimum price
    When I set the price from 60 with no maximum
    And I press Filter
    Then I see exactly these products: Red T-shirt Extra, Jeans Extra

  Scenario: Nothing matches
    When I tick Man and Shirt
    And I press Filter
    Then I see no products

  Scenario: Clearing the filters shows everything again
    Given I have filtered by Woman
    When I untick every box, set both prices to 0 and press Filter
    Then I see 9 products
