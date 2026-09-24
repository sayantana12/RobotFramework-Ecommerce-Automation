*** Settings ***
Documentation    PAGE OBJECT for https://automationexercise.com/view_cart
Library    SeleniumLibrary
Library    Collections
Library    String
Resource   ../Resources/variables.resource

*** Variables ***
${CART_TABLE}          id:cart_info
${CART_PRODUCT_ROWS}   css:#cart_info tbody tr
${CART_PRODUCT_NAME}   css:.cart_description h4 a

*** Keywords ***
Open Cart Page
    Go To    ${URL}/view_cart
    Wait Until Page Contains Element    ${CART_TABLE}    timeout=${TIMEOUT}

Get Cart Item Count
    ${count}=    Get Element Count    ${CART_PRODUCT_ROWS}
    RETURN    ${count}

Cart Should Contain At Least One Product
    Wait Until Page Contains Element    ${CART_TABLE}    timeout=${TIMEOUT}
    ${count}=    Get Cart Item Count
    Should Be True    ${count} > 0    msg=Expected at least one product in the cart but found none.

Cart Should Contain Product
    [Documentation]    Compare product names after normalizing whitespace.
    [Arguments]    ${product_name}
    Wait Until Page Contains Element    ${CART_PRODUCT_NAME}    timeout=${TIMEOUT}
    ${expected}=    Replace String Using Regexp    ${product_name}    \\s+    ${SPACE}
    ${expected}=    Strip String    ${expected}
    @{elements}=    Get WebElements    ${CART_PRODUCT_NAME}
    @{names}=    Create List
    FOR    ${element}    IN    @{elements}
        ${actual}=    Get Text    ${element}
        ${actual}=    Replace String Using Regexp    ${actual}    \\s+    ${SPACE}
        ${actual}=    Strip String    ${actual}
        Append To List    ${names}    ${actual}
    END
    Log To Console    Expected product: ${expected}
    Log To Console    Actual cart products: ${names}
    List Should Contain Value    ${names}    ${expected}    msg=Expected product '${expected}' was not found in the cart. Actual products: ${names}

Remove All Products From Cart
    [Documentation]    Empty the cart before each shopping journey to avoid false positives.
    Go To    ${URL}/view_cart

    FOR    ${attempt}    IN RANGE    30
        ${count}=    Get Element Count    ${CART_PRODUCT_ROWS}

        IF    ${count} == 0
            RETURN
        END

        Click Element    css:#cart_info tbody tr:first-child a.cart_quantity_delete

        Wait Until Keyword Succeeds    ${TIMEOUT}    500ms    Cart Should Be Empty
    END

    Fail    Cart still contains items after 30 deletion attempts.

Cart Should Be Empty
    ${count}=    Get Element Count    ${CART_PRODUCT_ROWS}
    Should Be Equal As Integers    ${count}    0