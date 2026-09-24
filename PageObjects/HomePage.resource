*** Settings ***
Library    SeleniumLibrary
Resource    ../Resources/variables.resource

*** Variables ***
${SIGNUP_LOGIN_LINK}        css:a[href="/login"]
${PRODUCTS_NAV_LINK}        css:a[href="/products"]
${CART_NAV_LINK}            css:a[href="/view_cart"]
${LOGOUT_LINK}              css:a[href="/logout"]
${HOME_LOGGED_IN_AS_TEXT}   xpath://a[contains(.,"Logged in as")]

*** Keywords ***
Open Home Page
    Go To    ${URL}
    Wait Until Element Is Visible    ${SIGNUP_LOGIN_LINK}    timeout=${TIMEOUT}

User Should Be Logged In As
    [Arguments]    ${username}
    Wait Until Element Is Visible    ${HOME_LOGGED_IN_AS_TEXT}    timeout=${TIMEOUT}
    Element Should Contain    ${HOME_LOGGED_IN_AS_TEXT}    ${username}

Logout From Application
    Wait Until Element Is Visible    ${LOGOUT_LINK}    timeout=${TIMEOUT}
    Click Element    ${LOGOUT_LINK}
    Wait Until Element Is Not Visible    ${HOME_LOGGED_IN_AS_TEXT}    timeout=${TIMEOUT}
    Wait Until Element Is Visible    ${SIGNUP_LOGIN_LINK}    timeout=${TIMEOUT}
