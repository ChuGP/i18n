*** Settings ***
Force Tags    ElementTextShouldBe
Resource    ../CommonVariables.txt
Resource    ./Keywords.txt
Library    SeleniumLibrary
Library    ../self_util.py
Test Setup    Run Keywords    Open Browser To Microsoft Page
...                    AND    Change Language    expectedLanguage=${language}
Test Teardown    Close Browser

*** Test Cases ***
Verify text of support button is expected
    Go To Support Page
    ${supportButton} =    Set Variable    //*[@id = 'uhfCatLogo' ]
    Element Text Should Be    ${supportButton}    Support
