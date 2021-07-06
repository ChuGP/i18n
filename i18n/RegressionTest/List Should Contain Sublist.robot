*** Settings ***
Force Tags    ElementShouldBeEqual
Resource    ../CommonVariables.txt
Library    SeleniumLibrary
Library    Collections
Library    ../self_util.py

*** Test Cases ***
List should contain sublist
    @{list1} =    Create List    Support    Support    Software
    @{list2} =    Create List    Support    Software
    List Should Contain Sub List    ${list1}    ${list2}