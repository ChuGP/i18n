*** Settings ***
Resource    ../CommonVariables.txt
Library    SeleniumLibrary
Library    ../self_util.py
Test Setup    Run Keywords    Open Browser To Microsoft Page
...                    AND    Change Language    expectedLanguage=${language}
Test Teardown    Close Browser

*** Test Cases ***
Test web element is on th support page by given special attributes
    Go To Support Page
    ${MicrosoftSupport} =    Set Variable    //*[@id ='supHomeAndLandingPageSearchBox' and @placeholder ='How can we help you?']
    Page Should Contain Element    ${MicrosoftSupport}

Check "Microsoft Support" webelement is on the support page
    Go To Support Page
    ${MicrosoftSupport} =    Set Variable    //*[@id ='supHomeAndLandingPageHeaderContainer']//*[contains(text(), 'Support')]
    Page Should Contain Element    ${MicrosoftSupport}


*** Keywords ***
Open Browser To Microsoft Page
    ${microsoftUrl} =    Set Variable    https://www.microsoft.com/
    ${microsoftLogo} =    Set Variable    //*[@id = 'uhfLogo']
    Run Keywords    Open Browser    ${MicrosoftUrl}    ${browser}
    ...             AND     Maximize Browser Window
    ...             AND    Wait Until Element Is Visible    ${microsoftLogo}

Click Element After It Is Visible
    [Arguments]    ${locator}
    Wait Until Page Contains Element    ${locator}    timeout=${shortPeriodOfTime}    error=${locator} should be visible.\n
    Wait Until Element Is Visible    ${locator}    timeout=${shortPeriodOfTime}    error=${locator} should be visible.\n
    Click Element    ${locator}

Change Language
    [Arguments]    ${expectedLanguage}
    ${languageOption} =    Set Variable    //a[contains(normalize-space(),'${expectedLanguage}')]
    ${changeToExpectedLanguage} =    Set Variable    xpath://*[contains(@class, 'global-head')]
    Scroll To The End
    Open Language Setting Menu
    Click Element After It Is Visible    ${languageOption}
    Wait Until Element Is Visible    ${changeToExpectedLanguage}    timeout=${shortPeriodOfTime}

Open Language Setting Menu
    ${languageLink} =    Set Variable    //*[@id='locale-picker-link']
    ${languageOptions} =    Set Variable    //*[contains(@class,'loc')]
    Click Element After It Is Visible    ${languageLink}
    Wait Until Element Is Visible    ${languageOptions}    timeout=${shortPeriodOfTime}

Go To Support Page
    Click Support Button
    Support Page Should Be Shown

Click Support Button
    ${supportButton} =    Set Variable    //*[@id = 'l1_support' ]
    Click Element After It Is Visible    ${supportButton}

Support Page Should Be Shown
    ${supportPage} =    Set Variable    //*[@id = 'uhfCatLogo']
    Wait Until Page Contains Element    ${supportPage}    timeout=${shortPeriodOfTime}    error=Support Page should be visible.\n
    Wait Until Element Is Visible    ${supportPage}    timeout=${shortPeriodOfTime}    error=Support Page should be visible.\n