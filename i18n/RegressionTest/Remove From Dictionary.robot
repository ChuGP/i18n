*** Settings ***
Force Tags    ElementShouldBeEqual
Resource    ../CommonVariables.txt
Library    SeleniumLibrary
Library    Collections
Library    ../self_util.py

*** Test Cases ***
Remove from dict
    &{dict1} =    Create Dictionary    Support=Software    Software=A
    Remove From Dictionary    ${dict1}    Support    A  # A 會被忽略
    Log    ${dict1}