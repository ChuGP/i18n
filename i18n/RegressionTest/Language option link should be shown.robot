*** Settings ***
Force Tags    Language
Resource    ../CommonVariables.txt
Resource    ./keywords.txt
Library    SeleniumLibrary
Library    ../self_util.py
Test Setup    Open Browser To Microsoft Page
Test Teardown    Close Browser

*** Test Cases ***
Change Language setting to expected language
    Change Language    expectedLanguage=${language}