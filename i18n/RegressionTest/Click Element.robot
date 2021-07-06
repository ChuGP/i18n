*** Settings ***
Force Tags    FindElement
Resource    ../CommonVariables.txt
Resource    ./keywords.txt
Library    Dialogs
Library    SeleniumLibrary
Library    ../self_util.py
Test Setup    Run Keywords    Open Browser To Microsoft Page
...                    AND    Change Language    expectedLanguage=${language}
Test Teardown    Close Browser

*** Test Cases ***
Go To Windows Page
    Click Windows Button
    Windows Page Should Be Shown

Click Microsoft Support Button On Support Page
    #要顯示support存在一詞多義
    Click Support Button
    Support Page Should Be Shown
    Click Microsoft Support Button
    Page Should Be The Same

*** Keywords ***
Click Windows Button
    ${windowsButton} =    Set Variable    //*[text()='Windows' and contains(@class, 'c-uhf-nav-link')]
    Click Element After It Is Visible    ${windowsButton}

Windows Page Should Be Shown
    ${supportPage} =    Set Variable    //*[@id = 'home-hero-item']
    Wait Until Page Contains Element    ${supportPage}    timeout=${shortPeriodOfTime}    error=Windows Page should be visible.\n
    Wait Until Element Is Visible    ${supportPage}    timeout=${shortPeriodOfTime}    error=Windows Page should be visible.\n

Click Microsoft Support Button
    ${microsoftSupportButton} =    Set Variable    //*[contains(@class, 'logo')]//span[contains(text(), 'Support')]
    Click Element After It Is Visible    ${microsoftSupportButton}

Page Should Be The Same
    Support Page Should Be Shown