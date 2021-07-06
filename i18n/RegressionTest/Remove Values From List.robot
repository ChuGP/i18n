*** Settings ***
Force Tags    ElementShouldBeEqual
Resource    ../CommonVariables.txt
Library    SeleniumLibrary
Library    Collections
Library    ../self_util.py

*** Test Cases ***
Remove values from list
    @{list1} =    Create List    支援    Software
    Remove Values From List    ${list1}    Support
    List Should Not Contain Value    ${list1}    支援
    Log    ${list1}

Second test
    @{list1} =    Create List    Support    Software
    Remove Values From List    ${list1}    Support
    List Should Not Contain Value    ${list1}    Support
    Log    ${list1}