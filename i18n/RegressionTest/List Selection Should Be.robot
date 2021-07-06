*** Settings ***
Force Tags    ElementShouldBeEqual
Resource    ../CommonVariables.txt
Library    SeleniumLibrary
Library    Collections
Library    ../self_util.py
Test Setup    Run Keywords    Open Browser    https://ssl-ezscrum.csie.ntut.edu.tw/ezScrum/    Chrome
              ...      AND    Maximize Browser Window
              ...      AND    Wait Until Element Is Visible    //*[@name='userId']
              ...      AND    Input Text     //*[@name='userId']    binchen561
              ...      AND    Input Text    //*[@name='password']    qwer3asdf4
              ...      AND    Click Button    //*[@name='Next']

*** Test Cases ***
List selection should be
    Wait Until Element Is Visible    //*[contains(@class, 'x-grid3-cell-inner') and normalize-space()='CapstoneRobotTest2']    ${shortPeriodOfTime}
    Double Click Element    //*[contains(@class, 'x-grid3-cell-inner') and normalize-space()='CapstoneRobotTest2']
    Wait Until Element Is Visible    //*[@id='Project_Top_Panel']    ${shortPeriodOfTime}
    Wait Until Element Is Visible    //*[@class='x-tree-node-anchor']//*[normalize-space()='TaskBoard']    ${shortPeriodOfTime}
    Double Click Element    //*[@class='x-tree-node-anchor']//*[normalize-space()='Scrum Report']
    List Selection Should Be Sprint 20
    [Teardown]    Close Browser

*** Keywords ***
List Selection Should Be Sprint 20
    Select Frame    xpath://iframe[@id='remainingWorkReport']
    # List Selection Should Be    //*[@id='ShowSprint']    Sprint 19
    List Selection Should Be    //*[@id='ShowSprint']    Sprint 21
    [Teardown]    Unselect Frame