
*** Settings ***
Documentation    PAGE OBJECT for https://automationexercise.com/products
...              Product catalogue, search, and Add to Cart modal.
Library    SeleniumLibrary
Resource   ../Resources/variables.resource

*** Variables ***
${SEARCH_INPUT_FIELD}         id:search_product
${SEARCH_SUBMIT_BUTTON}       id:submit_search
${SEARCHED_PRODUCTS_TITLE}    xpath://h2[contains(text(),"Searched Products")]
${PRODUCT_CARD}               xpath://div[@class="product-image-wrapper"]
${MODAL_VIEW_CART_LINK}       xpath://div[@class="modal-content"]//u[text()="View Cart"]/parent::a
${MODAL_CONTINUE_SHOPPING}    css:.modal-content .btn-success.close-modal

*** Keywords ***
Open Products Page
    Go To    ${URL}/products
    Wait Until Page Contains    All Products    timeout=${TIMEOUT}

Search For Product
    [Arguments]    ${product_name}
    Input Text    ${SEARCH_INPUT_FIELD}    ${product_name}
    Click Button    ${SEARCH_SUBMIT_BUTTON}
    Wait Until Page Contains Element    ${SEARCHED_PRODUCTS_TITLE}    timeout=${TIMEOUT}

Search Results Should Not Be Empty
    ${count}=    Get Element Count    ${PRODUCT_CARD}
    Should Be True    ${count} > 0    msg=No products were found for the given search term.

Add Product To Cart By Index
    [Arguments]    ${index}=1
    [Documentation]    Add the Nth product, using JavaScript if an ad intercepts the click.
    ${card}=    Set Variable    xpath:(//div[contains(@class,"product-image-wrapper")])[${index}]
    ${add_link}=    Set Variable    ${card}//div[contains(@class,"productinfo")]//a[contains(@class,"add-to-cart")]

    Wait Until Element Is Visible    ${card}    timeout=${TIMEOUT}
    Scroll Element Into View    ${card}
    Execute Javascript    window.scrollBy(0, -150);
    Wait Until Element Is Visible    ${add_link}    timeout=${TIMEOUT}

    ${clicked}=    Run Keyword And Return Status    Click Element    ${add_link}

    IF    not ${clicked}
        Log    Normal Add to Cart click was intercepted; trying JavaScript click.    WARN
        ${button}=    Get WebElement    ${add_link}
        Execute Javascript    arguments[0].click();    ARGUMENTS    ${button}
    END

    Wait Until Element Is Visible    ${MODAL_VIEW_CART_LINK}    timeout=${TIMEOUT}

Continue Shopping From Modal
    Click Element    ${MODAL_CONTINUE_SHOPPING}
    Wait Until Element Is Not Visible    ${MODAL_CONTINUE_SHOPPING}    timeout=${TIMEOUT}

Go To Cart From Modal
    [Documentation]    Open the cart, using JavaScript if an advertisement intercepts the click.
    Wait Until Element Is Visible    ${MODAL_VIEW_CART_LINK}    timeout=${TIMEOUT}

    ${clicked}=    Run Keyword And Return Status
    ...    Click Element    ${MODAL_VIEW_CART_LINK}

    IF    not ${clicked}
        Log    Normal View Cart click was intercepted; trying JavaScript click.    WARN
        ${cart_link}=    Get WebElement    ${MODAL_VIEW_CART_LINK}
        Execute Javascript    arguments[0].click();    ARGUMENTS    ${cart_link}
    END

    Wait Until Location Contains    /view_cart    timeout=${TIMEOUT}

Get Product Name By Index
    [Arguments]    ${index}=1
    ${name_locator}=    Set Variable    xpath:(//div[contains(@class,"product-image-wrapper")])[${index}]//div[contains(@class,"productinfo")]//p
    Wait Until Element Is Visible    ${name_locator}    timeout=${TIMEOUT}
    ${name}=    Get Text    ${name_locator}
    RETURN    ${name}