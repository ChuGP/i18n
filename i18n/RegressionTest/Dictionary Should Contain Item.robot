*** Settings ***
Force Tags    ElementShouldBeEqual
Resource    ../CommonVariables.txt
Library    SeleniumLibrary
Library    Collections
Library    ../self_util.py

*** Test Cases ***
Dictionary should contain item
    &{dict1} =    Create Dictionary    More=Support
    Dictionary Should Contain Item    ${dict1}    More    Support

Dictionary should contain key
    &{dict1} =    Create Dictionary    Support=Software
    Dictionary Should Contain Key    ${dict1}    Support

Dictionary should not contain key
    &{dict1} =    Create Dictionary    Support=Software
    Dictionary Should Not Contain Key    ${dict1}    test

Dictionary should contain value
    &{dict1} =    Create Dictionary    Software=Support
    Dictionary Should Contain Value    ${dict1}    Support

Dictionary should not contain value
    &{dict1} =    Create Dictionary    Software=Support
    Dictionary Should Not Contain Value    ${dict1}    test