*** Settings ***
Force Tags    ListShouldBeEqual
Resource    ../CommonVariables.txt
Resource    ./keywords.txt
Library    Collections
Library    SeleniumLibrary
Library    ../self_util.py
Test Setup    Run Keywords    Open Browser To Microsoft Page
...                    AND    Change Language    expectedLanguage=${language}
...                    AND    Go To Support Page
Test Teardown    Close Browser

*** Variables ***
@{expectedMenuTopBarTexts} =    Software    PCs & Devices    Entertainment    Business    Developer&IT    Other

*** Test Cases ***
Check Menu TopBar Texts are expected
    Open More Menu
    ${menuTopBarButtons} =    Set Variable    //*[contains(@id, 'uhf-navspn-shellmenu')]
    ${menuTopBarTexts} =    Get TopBarButtons Text    ${menuTopBarButtons}
    Lists Should Be Equal    ${expectedMenuTopBarTexts}    ${menuTopBarTexts}

Lists should be equal
    @{list1} =    Set Variable    Software    Support
    @{list2} =    Set Variable    Software    Support
    Lists Should Be Equal    ${list1}    ${list2}

*** Keywords ***
Open More Menu
    ${moreButton} =    Set Variable    //button[contains(normalize-space(), 'All Microsoft')]
    Sleep    1s
    Click Element After It Is Visible    ${moreButton}
    Wait Until Element Is Visible    //*[contains(@class, 'f-multi-column') and @aria-hidden='false']    timeout=${shortPeriodOfTime}    error= All Microsoft menu should be visible.


Get TopBarButtons Text
    [Arguments]    ${menuTopBarButtons}
    ${menuTopBarTexts} =    Get Texts After Page Contain Element    ${menuTopBarButtons}
    [Return]    ${menuTopBarTexts}