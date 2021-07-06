*** Settings ***
Force Tags    ElementShouldBeEqual
Resource    ../CommonVariables.txt
Resource    ./keywords.txt
Library    Collections
Library    SeleniumLibrary
Library    ../self_util.py
# Test Setup    Run Keywords    Open Browser To Microsoft Page
# ...                    AND    Change Language    expectedLanguage=${language}
# Test Teardown    Close Browser

*** Test Cases ***
Check office TopBar Dropdown contanis "Products"
    Go To Office Page
    ${officeTopBarDropdown} =    Get Texts After Page Contain Element    //button[@id and not(@class)]
    Should Contain    ${officeTopBarDropdown}    Products

TopBar List contain multiple meaning of the word
    Go To Support Page
    ${commonTopBarButtons} =    Set Variable    //a[@class = 'c-uhf-nav-link' and not(@id ='shellmenu_4') or @id = 'uhfCatLogo']
    ${commonTopBarTexts} =    Get Texts After Page Contain Element    ${commonTopBarButtons}
    Should Contain    ${commonTopBarTexts}    Support

Test should contain
    @{list1} =    Set Variable    Support    Software
    Should Contain    ${list1}    Support