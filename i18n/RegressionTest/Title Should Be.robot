*** Settings ***
Force Tags    TitleShouldBe
Resource    ../CommonVariables.txt
Library    SeleniumLibrary
Library    Collections
Library    ../self_util.py
Test Setup    Run Keywords    Open Browser    http://localhost:3000    Chrome
...                    AND    Maximize Browser Window
Test Teardown    Close Browser

*** Test Cases ***
Title Should Be
    ${pageHeader} =    Set Variable    //*[normalize-space()='I18n Testing Website']
    Wait Until Element Is Visible    ${pageHeader}    timeout=${shortPeriodOfTime}
    Title Should Be    I18n Web Testing
