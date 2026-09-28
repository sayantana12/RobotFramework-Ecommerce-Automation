from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


VALID_USERNAME = "standard_user"
VALID_PASSWORD = "secret_sauce"
LOCKED_USERNAME = "locked_out_user"
EXPECTED_LOCKED_ERROR = "Epic sadface: Sorry, this user has been locked out."


def save_screenshot(driver, screenshot_dir, filename):
    path = Path(screenshot_dir) / filename
    driver.save_screenshot(str(path))
    print(f"[SHOT] {path}")


def test_valid_login(driver, screenshot_dir):
    login_page = LoginPage(driver).open()
    login_page.login(VALID_USERNAME, VALID_PASSWORD)

    inventory_page = InventoryPage(driver)

    # Assertions stay in the test layer; page objects only expose UI behavior.
    assert inventory_page.is_loaded()
    assert inventory_page.get_first_product_name() == "Sauce Labs Backpack"

    save_screenshot(driver, screenshot_dir, "01_valid_login.png")


def test_locked_user_error(driver, screenshot_dir):
    login_page = LoginPage(driver).open()
    login_page.login(LOCKED_USERNAME, VALID_PASSWORD)

    error_message = login_page.get_error_message()

    assert error_message == EXPECTED_LOCKED_ERROR

    save_screenshot(driver, screenshot_dir, "02_locked_user_error.png")


def test_logout_flow(driver, screenshot_dir):
    login_page = LoginPage(driver).open()
    login_page.login(VALID_USERNAME, VALID_PASSWORD)

    inventory_page = InventoryPage(driver)
    assert inventory_page.is_loaded()

    inventory_page.logout()

    # Assertion remains in the test class/function, not inside a page object.
    login_btn = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "login-button"))
    )
    assert login_btn.is_displayed()

    save_screenshot(driver, screenshot_dir, "03_logout_returned_to_login.png")
