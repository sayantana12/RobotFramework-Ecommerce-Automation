
*** Settings ***
Documentation    Capstone: browser -> login -> search -> cart -> verify -> logout -> close.

Resource    ../Resources/variables.resource
Resource    ../Resources/common.resource
Resource    ../PageObjects/HomePage.resource
Resource    ../PageObjects/LoginPage.resource
Resource    ../PageObjects/ProductsPage.resource
Resource    ../PageObjects/CartPage.resource

Library     OperatingSystem
Library     String
Library     Collections

Test Setup       Open Application
Test Teardown    Finish Test


*** Variables ***
${SEARCH_DATA_FILE}    ${CURDIR}/../TestData/search_products.csv


*** Test Cases ***

Complete Purchase Journey For One Product
    [Documentation]    Complete the shopping journey for Dress.
    [Tags]    e2e    smoke

    Run Shopping Journey    Dress


Complete Purchase Journey For Every Product In The Data File
    [Documentation]    Test Dress, Top and Saree in one login session.
    [Tags]    e2e    data-driven    regression

    @{rows}=    Read Search Rows From File    ${SEARCH_DATA_FILE}

    # Log in only once.
    Login With Existing Account

    FOR    ${term}    ${minimum}    IN    @{rows}

        Log To Console    Testing search term: ${term}

        # Clear the cart before testing each product.
        Remove All Products From Cart

        Open Products Page

        Search For Product    ${term}

        Search Results Should Meet Minimum    ${minimum}

        ${product_name}=    Get Product Name By Index    1

        Add Product To Cart By Index    1

        Go To Cart From Modal

        Cart Should Contain Product    ${product_name}

        Log To Console    Successfully verified: ${product_name}

    END

    # Log out only after all products have been tested.
    Logout From Application


*** Keywords ***

Run Shopping Journey
    [Documentation]    Complete a shopping journey for one product.
    [Arguments]    ${term}    ${minimum}=1

    Login With Existing Account

    Remove All Products From Cart

    Open Products Page

    Search For Product    ${term}

    Search Results Should Meet Minimum    ${minimum}

    ${product_name}=    Get Product Name By Index    1

    Add Product To Cart By Index    1

    Go To Cart From Modal

    Cart Should Contain Product    ${product_name}

    Logout From Application


Search Results Should Meet Minimum
    [Arguments]    ${minimum}

    ${count}=    Get Element Count    ${PRODUCT_CARD}

    ${minimum}=    Convert To Integer    ${minimum}

    Should Be True
    ...    ${count} >= ${minimum}
    ...    msg=Only ${count} products found; expected at least ${minimum}.


Read Search Rows From File
    [Arguments]    ${path}

    ${content}=    Get File    ${path}

    @{lines}=    Split To Lines    ${content}

    @{rows}=    Create List

    FOR    ${line}    IN    @{lines}[1:]

        ${line}=    Strip String    ${line}

        IF    not $line
            CONTINUE
        END

        @{parts}=    Split String    ${line}    ,

        Length Should Be
        ...    ${parts}
        ...    2
        ...    msg=Each CSV row must contain search_term,min_expected_results.

        Append To List    ${rows}    ${parts[0]}

        Append To List    ${rows}    ${parts[1]}

    END

    RETURN    ${rows}