*** Settings ***
Documentation    Login tests using a previously registered account; no automatic signup.
Resource    ../Resources/variables.resource
Resource    ../Resources/common.resource
Resource    ../PageObjects/HomePage.resource
Resource    ../PageObjects/LoginPage.resource
Test Setup       Open Application
Test Teardown    Finish Test

*** Test Cases ***
Login With Valid Credentials
    [Tags]    login    smoke    positive
    Login With Existing Account
    Logout From Application

Login Should Fail For Invalid Credentials
    [Template]    Attempt Login And Expect Error
    [Tags]    login    negative    data-driven
    nonexistent.user@example.com    SomePassword@123
    ${TEST_USER_EMAIL}    ${INVALID_PASSWORD}
    another.fake.user@example.com    abc123

*** Keywords ***
Attempt Login And Expect Error
    [Arguments]    ${email}    ${password}
    Login With Credentials    ${email}    ${password}
    Login Error Should Be Displayed
