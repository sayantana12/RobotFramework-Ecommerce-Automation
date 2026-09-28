"""
Assignment 9: PyTest Integration with HTML Reporting
Site       : https://the-internet.herokuapp.com/login
Framework  : pytest + Selenium WebDriver
Reporting  : pytest-html
Screenshots: screenshot_a9/

Run normally:
    pytest assignment9.py

Run the intentional failure demo:
    pytest assignment9.py --demo-failure -k failure_screenshot_demo
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "https://the-internet.herokuapp.com/login"
USERNAME = "tomsmith"
PASSWORD = "SuperSecretPassword!"
TIMEOUT = 10


def open_login_page(driver):
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, TIMEOUT)
    wait.until(EC.visibility_of_element_located((By.ID, "username")))
    wait.until(EC.visibility_of_element_located((By.ID, "password")))
    return wait


def test_valid_login(driver):
    """Verify that valid credentials open the Secure Area."""
    wait = open_login_page(driver)

    driver.find_element(By.ID, "username").send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    flash = wait.until(EC.visibility_of_element_located((By.ID, "flash")))
    assert "You logged into a secure area!" in flash.text
    assert "secure" in driver.current_url
    assert driver.find_element(By.TAG_NAME, "h2").text == "Secure Area"


def test_invalid_username(driver):
    """Verify the validation message for an incorrect username."""
    wait = open_login_page(driver)

    driver.find_element(By.ID, "username").send_keys("invalid_user")
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    flash = wait.until(EC.visibility_of_element_located((By.ID, "flash")))
    assert "Your username is invalid!" in flash.text


def test_invalid_password(driver):
    """Verify the validation message for an incorrect password."""
    wait = open_login_page(driver)

    driver.find_element(By.ID, "username").send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys("wrong_password")
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    flash = wait.until(EC.visibility_of_element_located((By.ID, "flash")))
    assert "Your password is invalid!" in flash.text


def test_logout_after_valid_login(driver):
    """Verify that a valid session can be ended using Logout."""
    wait = open_login_page(driver)

    driver.find_element(By.ID, "username").send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/logout']"))).click()
    wait.until(EC.visibility_of_element_located((By.ID, "username")))

    assert "/login" in driver.current_url
    assert driver.find_element(By.TAG_NAME, "h2").text == "Login Page"


def test_failure_screenshot_demo(driver, request):
    """Intentional failure used only to demonstrate automatic screenshot capture."""
    if not request.config.getoption("--demo-failure"):
        pytest.skip("Run with --demo-failure to demonstrate failed-step screenshot capture.")

    open_login_page(driver)

    # This assertion is intentionally wrong so the hook captures a screenshot.
    assert driver.title == "This title is intentionally incorrect"
