*** Settings ***
Force Tags    SelectFromListByValue
Resource    ../CommonVariables.txt
Library    SeleniumLibrary
Test Setup    Run Keywords    Go To I18n Testing Website
Test Teardown    Close Browser

*** Test Cases ***
Select from list by the value "2"
    ${selectionList} =    Set Variable    //*[@id='i18n-selection-list']
    Wait Until Element Is Visible    ${defaultSelection}    timeout=${shortPeriodOfTime}
    Select From List By Value    ${selectionList}    2
    List Selection Should Be    ${selectionList}    Support

*** Keywords ***
Go To I18n Testing Website
    Open Browser    http://localhost:3000    Chrome
    Maximize Browser Window

*** Variables ***
${defaultSelection} =    //*[@id='i18n-selection-list']//*[text()='Software' and @selected]
