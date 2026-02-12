Feature: Registration page


  Scenario: The user can enter the information into the input fields on the registration page
    Given Open the registration page
    When I enter some test information into the registration fields
    Then Verify the right information is present in the fields
