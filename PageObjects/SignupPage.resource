*** Settings ***
Documentation    PAGE OBJECT for the "ENTER ACCOUNT INFORMATION" form shown after submitting
...              the initial signup form, plus the "Account Created!" and "Account Deleted!"
...              confirmation pages that follow account creation / deletion.
Library    SeleniumLibrary
Resource   ../Resources/variables.resource

*** Variables ***
${TITLE_MR_RADIO}          id:id_gender1
${ACCOUNT_PASSWORD_FIELD}  id:password
${DOB_DAY}                 id:days
${DOB_MONTH}               id:months
${DOB_YEAR}                id:years
${FIRST_NAME_FIELD}        id:first_name
${LAST_NAME_FIELD}         id:last_name
${ADDRESS_FIELD}           id:address1
${STATE_FIELD}             id:state
${CITY_FIELD}              id:city
${ZIPCODE_FIELD}           id:zipcode
${MOBILE_NUMBER_FIELD}     id:mobile_number
${CREATE_ACCOUNT_BUTTON}   css:button[data-qa="create-account"]
${ACCOUNT_CREATED_TEXT}    css:[data-qa="account-created"]
${CONTINUE_BUTTON}         css:[data-qa="continue-button"]
${DELETE_ACCOUNT_LINK}     css:a[href="/delete_account"]
${ACCOUNT_DELETED_TEXT}    css:[data-qa="account-deleted"]

*** Keywords ***
Fill Mandatory Account Details
    [Arguments]    ${password}    ${day}    ${month}    ${year}
    Click Element    ${TITLE_MR_RADIO}
    Input Text    ${ACCOUNT_PASSWORD_FIELD}    ${password}
    Select From List By Value    ${DOB_DAY}    ${day}
    Select From List By Value    ${DOB_MONTH}    ${month}
    Select From List By Value    ${DOB_YEAR}    ${year}

Fill Address Details
    [Arguments]    ${first_name}    ${last_name}    ${address}    ${state}    ${city}    ${zipcode}    ${mobile}
    Input Text    ${FIRST_NAME_FIELD}    ${first_name}
    Input Text    ${LAST_NAME_FIELD}    ${last_name}
    Input Text    ${ADDRESS_FIELD}    ${address}
    Input Text    ${STATE_FIELD}    ${state}
    Input Text    ${CITY_FIELD}    ${city}
    Input Text    ${ZIPCODE_FIELD}    ${zipcode}
    Input Text    ${MOBILE_NUMBER_FIELD}    ${mobile}

Submit Create Account
    Click Button    ${CREATE_ACCOUNT_BUTTON}

Account Should Be Created
    Wait Until Page Contains Element    ${ACCOUNT_CREATED_TEXT}    timeout=${TIMEOUT}

Click Continue After Account Creation
    Click Element    ${CONTINUE_BUTTON}

Delete Test Account
    Click Element    ${DELETE_ACCOUNT_LINK}
    Wait Until Page Contains Element    ${ACCOUNT_DELETED_TEXT}    timeout=${TIMEOUT}
    Click Element    ${CONTINUE_BUTTON}
