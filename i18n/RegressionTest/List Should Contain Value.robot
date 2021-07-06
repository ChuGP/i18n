*** Settings ***
Force Tags    ElementShouldBeEqual
Resource    ../CommonVariables.txt
Library    SeleniumLibrary
Library    Collections
Library    ../self_util.py

*** Test Cases ***
List should contain value
    @{list1} =    Create List    Software    Support
    # Log    ${dict1}
    List Should Contain Value    ${list1}    Support

List should not contain value
    @{list1} =    Create List    Support
    # Log    ${dict1}
    List Should Not Contain Value    ${list1}    Software