@echo off
set "BROWSER=%~1"
if "%BROWSER%"=="" set "BROWSER=chrome"
robot --variable BROWSER:%BROWSER% --outputdir Results TestSuites/02_login_tests.robot TestSuites/03_ecommerce_business_flow.robot
exit /b %ERRORLEVEL%
