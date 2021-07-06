*** Settings ***
Force Tags    ElementShouldBeEqual
Resource    ../CommonVariables.txt
Library    SeleniumLibrary
Library    Collections
Library    ../self_util.py

*** Test Cases ***
Dictionaries should be equal
    # &{dict1} =    Create Dictionary    Software=支援
    # &{dict1} =    Create Dictionary    Software=Support
    # &{dict1} =    Create Dictionary    Software=Support    A=B
    &{dict1} =    Create Dictionary    軟體=支援
    &{dict2} =    Create Dictionary    Software=Support
    Dictionaries Should Be Equal    ${dict1}    ${dict2}

Dictionary should contain sub dictionary
    &{dict1} =    Create Dictionary    Software=Support    A=B
    &{dict2} =    Create Dictionary    Software=Support
    Dictionary Should Contain Sub Dictionary    ${dict1}    ${dict2}