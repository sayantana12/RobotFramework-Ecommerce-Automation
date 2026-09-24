*** Settings ***
Documentation    Global, project-wide variables.
...              Centralising these here means every resource file and test suite
...              refers to the SAME values, and the whole suite can be re-pointed at
...              a different browser / environment / account by changing only this file
...              (or by overriding a value from the command line / Jenkins, see README.md).

*** Variables ***
# ---- Environment ------------------------------------------------------
${BROWSER}              chrome
${URL}                  https://automationexercise.com
${TIMEOUT}              15s
${DELAY}                0s

# ---- Persistent test account -------------------------------------------
# Used by the Login suite and the End-to-End suite. The %{VAR=default} syntax
# reads an OS environment variable if one is set (e.g. injected by Jenkins
# credentials) and silently falls back to the given default otherwise.
# This means real credentials never have to be hard-coded in source control.
${TEST_USER_NAME}       %{RF_TEST_NAME=Robot Tester}
${TEST_USER_EMAIL}      %{RF_TEST_EMAIL=robot.tester.capstone@example.com}
${TEST_USER_PASSWORD}   %{RF_TEST_PASSWORD=RobotTest@123}

# ---- Misc test data ------------------------------------------------------
${INVALID_PASSWORD}     WrongPassword@999
