*** Settings ***
Library    Dialogs
Library    SeleniumLibrary
Library    ../self_util.py
Test Setup    Run Keywords    Open Browser    http:localhost:3000    Chrome
...                    AND    Maximize Browser Window
Test Teardown    Close Browser

*** Test Cases ***
Alert should be present
    Wait Until Element Is Visible    //*[normalize-space()='Show Alert Message']    timeout=3s
    Double Click Element    //*[normalize-space()='Show Alert Message']
    Alert Should Be Present    Welcome to Bing's website

# Input text into alert
    # Wait Until Element Is Visible    //*[normalize-space()='Show Alert Message']    timeout=3s
    # Double Click Element    //*[normalize-space()='Show Alert Message']
    # Input Text Into Alert    hello