*** Settings ***
Force Tags    ListShouldBeEqual
Resource    ../CommonVariables.txt
Resource    ./keywords.txt
Library    Collections
Library    SeleniumLibrary
Library    self_util
Test Setup    Run Keywords    Open Browser To Microsoft Page
...                    AND    Change Language    expectedLanguage=${language}
...                    AND    Go To Support Page
Test Teardown    Close Browser

*** Variables ***
@{expectedMenuTopBarTexts} =    Software    PCs & Devices    Entertainment    Business    Developer & IT    Other
@{expectedCommonTopBarTexts} =    Office    Windows    Surface    Xbox    Support

*** Test Cases ***
Check Menu TopBar Texts are expected
    Open More Menu
    ${menuTopBarButtons} =    Set Variable    //button[contains(@role,'presentation')]
    ${menuTopBarTexts} =    Get TopBarButtons Text    ${menuTopBarButtons}
    Lists Should Be Equal    ${expectedMenuTopBarTexts}    ${menuTopBarTexts}

*** Keywords ***
Open More Menu
    ${moreButton} =    Set Variable    //button[contains(normalize-space(), 'More')]
    ${menuTopBarButtons} =    Set Variable    //button[contains(@role,'presentation')]
    Click Element After It Is Visible    ${moreButton}
    ${isOpened} =    Run Keyword And Return Status    Wait Until Element Is Visible    ${menuTopBarButtons}    timeout=${shortPeriodOfTime}    error=More Menu should be visible.\n
    Run Keyword If    ${isOpened} == False    Open More Menu

Get TopBarButtons Text
    [Arguments]    ${menuTopBarButtons}
    ${topBarElements} =    Get WebElements    ${menuTopBarButtons}
    ${menuTopBarTexts} =    Get Texts After Page Contain Element    ${menuTopBarButtons}
    Run Keyword And Return If    ${menuTopBarTexts.__len__()} != ${topBarElements.__len__()}    Get TopBarButtons Text    ${menuTopBarButtons}
    [Return]    ${menuTopBarTexts}