*** Settings ***
Force Tags    FindElement
Resource    ../CommonVariables.txt
Resource    ./keywords.txt
Library    SeleniumLibrary
Library    self_util
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

*** Keywords ***
Get WebElement After It Is Visible
    [Arguments]    ${locator}
    Wait Until Page Contains Element    ${locator}    timeout=${normalPeriodOfTime}    error=${locator} should be visible.\n
    Wait Until Element Is Visible    ${locator}    timeout=${normalPeriodOfTime}    error={locator} should be visible.\n$
    Run Keyword And Return    Get WebElement     ${locator}