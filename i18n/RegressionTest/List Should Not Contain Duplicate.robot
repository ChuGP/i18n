*** Settings ***
Force Tags    ElementShouldBeEqual
Resource    ../CommonVariables.txt
Library    SeleniumLibrary
Library    Collections
Library    ../self_util.py

*** Test Cases ***
List should not contain duplicates
    @{list1} =    Create List    Software    Support
    # @{list1} =    Create List    Software    Support    Support
    # Log    ${dict1}
    List Should Not Contain Duplicates    ${list1}