*** Settings ***
Documentation    Browser lifecycle and reusable business-flow keywords.
Library    SeleniumLibrary
Resource    variables.resource
Resource    ../PageObjects/HomePage.resource
Resource    ../PageObjects/LoginPage.resource

*** Keywords ***
Open Application
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Timeout    ${TIMEOUT}
    Set Selenium Speed    ${DELAY}
    Open Home Page

Close Application
    Close All Browsers

Finish Test
    Run Keyword If Test Failed    Capture Page Screenshot    EMBED
    Close Application

Login With Existing Account
    Login With Credentials    ${TEST_USER_EMAIL}    ${TEST_USER_PASSWORD}
    User Should Be Logged In As    ${TEST_USER_NAME}

Finish Shopping Journey
    [Documentation]    Log out, verify logged-out state; test teardown closes browser.
    Logout From Application
