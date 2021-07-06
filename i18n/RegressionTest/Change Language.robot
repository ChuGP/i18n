*** Settings ***
Force Tags    Language
Resource    ../CommonVariables.txt
Library    SeleniumLibrary
Library    ../self_util.py
Test Setup    Open Browser To Microsoft Page
Test Teardown    Close Browser

*** Test Cases ***
Verify language setting menu can be opened
    Scroll To The End
    Open Language Setting Menu
    Language Setting Menu Should Be Shown

*** Keywords ***
Open Browser To Microsoft Page
    ${microsoftUrl} =    Set Variable    https://www.microsoft.com/
    ${microsoftLogo} =    Set Variable    //*[@id = 'uhfLogo']
    Run Keywords    Open Browser    ${MicrosoftUrl}    ${browser}
    ...             AND     Maximize Browser Window
    ...             AND    Wait Until Element Is Visible    ${microsoftLogo}

Open Language Setting Menu
    ${languageLink} =    Set Variable    //*[@id='locale-picker-link']
    ${languageSettingMenu} =    Set Variable    //*[contains(@class,'loc')]
    Click Element After It Is Visible    ${languageLink}
    Wait Until Element Is Visible    ${languageSettingMenu}    timeout=${shortPeriodOfTime}    error=Language Setting Menu should be visible.\n

Click Element After It Is Visible
    [Arguments]    ${locator}
    Wait Until Page Contains Element    ${locator}    timeout=${shortPeriodOfTime}    error=${locator} should be visible.\n
    Wait Until Element Is Visible    ${locator}    timeout=${shortPeriodOfTime}    error=${locator} should be visible.\n
    Click Element    ${locator}

Language Setting Menu Should Be Shown
    ${languageSettingMenu} =    Set Variable    //*[contains(@class,'loc')]
    Wait Until Page Contains Element    ${languageSettingMenu}    timeout=${shortPeriodOfTime}    error=Language Setting Menu should be visible.\n
    Wait Until Element Is Visible    ${languageSettingMenu}    timeout=${shortPeriodOfTime}    error=Language Setting Menu should be visible.\n

