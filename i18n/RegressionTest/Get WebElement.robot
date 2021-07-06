*** Settings ***
Force Tags    FindElement
Resource    ../CommonVariables.txt
Resource    ./keywords.txt
Library    SeleniumLibrary
Library    ../self_util.py
Test Setup    Run Keywords    Open Browser To Microsoft Page
...                    AND    Change Language    expectedLanguage=${language}
Test Teardown    Close Browser

*** Test Cases ***
Get Products Button Webelement
    Go To Office Page
    ${productsButton} =    Set Variable    //button[text()='Products']
    ${element} =    Get WebElement After It Is Visible    ${productsButton}
    ${text} =    Get Text After It Is Visible    ${element}
    Should Be Equal    Products    ${text}
