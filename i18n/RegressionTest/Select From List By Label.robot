*** Settings ***
Force Tags    SelectFromListByLabel
Resource    ../CommonVariables.txt
Library    SeleniumLibrary
Test Setup    Run Keywords    Open Browser    http://localhost:3000    Chrome
...                    AND    Maximize Browser Window
Test Teardown    Close Browser

*** Test Cases ***
Select from list by the label "Support"
    ${defaultSelection} =    Set Variable    //*[@id='i18n-selection-list']//*[text()='Software' and @selected]
    ${selectionList} =    Set Variable    //*[@id='i18n-selection-list']
    Wait Until Element Is Visible    ${defaultSelection}    timeout=${shortPeriodOfTime}
    Select From List By Label    ${selectionList}    Support
    List Selection Should Be    ${selectionList}    Support
