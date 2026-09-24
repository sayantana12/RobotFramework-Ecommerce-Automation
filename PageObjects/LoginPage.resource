*** Settings ***
Documentation    PAGE OBJECT for https://automationexercise.com/login
...              This single page hosts two forms side by side: "New User Signup!" and
...              "Login to your account". Locators for both live here since they belong
...              to the same physical page.
Library    SeleniumLibrary
Resource   ../Resources/variables.resource

*** Variables ***
# --- Login form ---
${LOGIN_EMAIL_FIELD}      css:input[data-qa="login-email"]
${LOGIN_PASSWORD_FIELD}   css:input[data-qa="login-password"]
${LOGIN_BUTTON}           css:button[data-qa="login-button"]
${LOGIN_ERROR_MSG}        xpath://form[@action="/login"]//p[contains(text(),"incorrect")]

# --- Signup form ---
${SIGNUP_NAME_FIELD}      css:input[data-qa="signup-name"]
${SIGNUP_EMAIL_FIELD}     css:input[data-qa="signup-email"]
${SIGNUP_BUTTON}          css:button[data-qa="signup-button"]
${SIGNUP_ERROR_MSG}       xpath://form[@action="/signup"]//p[contains(text(),"already exist")]

*** Keywords ***
Open Login Page
    Go To    ${URL}/login
    Wait Until Page Contains    Login to your account    timeout=${TIMEOUT}

Input Login Email
    [Arguments]    ${email}
    Input Text    ${LOGIN_EMAIL_FIELD}    ${email}

Input Login Password
    [Arguments]    ${password}
    Input Text    ${LOGIN_PASSWORD_FIELD}    ${password}

Click Login Button
    Click Button    ${LOGIN_BUTTON}

Login With Credentials
    [Arguments]    ${email}    ${password}
    [Documentation]    Convenience USER DEFINED KEYWORD that performs a complete login
    ...                (navigate + fill + submit) in a single call. Other keywords are
    ...                built out of smaller, single-purpose keywords on purpose - this one
    ...                shows how small keywords compose into a bigger, business-readable one.
    Open Login Page
    Input Login Email    ${email}
    Input Login Password    ${password}
    Click Login Button

Input Signup Name And Email
    [Arguments]    ${name}    ${email}
    Input Text    ${SIGNUP_NAME_FIELD}    ${name}
    Input Text    ${SIGNUP_EMAIL_FIELD}    ${email}

Click Signup Button
    Click Button    ${SIGNUP_BUTTON}

Login Error Should Be Displayed
    Wait Until Element Is Visible    ${LOGIN_ERROR_MSG}    timeout=${TIMEOUT}

Signup Error Should Be Displayed
    Wait Until Element Is Visible    ${SIGNUP_ERROR_MSG}    timeout=${TIMEOUT}
