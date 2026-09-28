"""
Assignment 1: The Multi-Locator Challenge
Site       : https://www.saucedemo.com/ (SauceDemo Login Page)
Focus      : Mastering element identification, synchronization, and basic browser actions.
Task       : Navigate to a login page (SauceDemo).
             Find and interact with:
             - Username field using By.ID ("user-name")
             - Password field using By.NAME ("password")
             - Login button using By.XPATH ("//input[@id='login-button']")
Validation : Assert that the resulting page URL contains '/inventory.html' after logging in.
Run        : python assignment1_multi_locator.py
"""

from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.saucedemo.com/"
VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"
TIMEOUT = 10
SCREENSHOT_DIR = Path(__file__).resolve().parent / "screenshot_a1"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


def shot(driver, name: str) -> Path:
    path = SCREENSHOT_DIR / f"{name}.png"
    driver.save_screenshot(str(path))
    print(f"[SHOT] saved -> {path}")
    return path


def test_multi_locator_login(driver):
    wait = WebDriverWait(driver, TIMEOUT)

    # Step 1: Navigate to login page
    print("\n--- Step 1: Navigating to SauceDemo Login Page ---")
    driver.get(BASE_URL)
    wait.until(EC.title_contains("Swag Labs"))
    print(f"[PASS] Page loaded: {driver.title} ({driver.current_url})")
    shot(driver, "01_login_page_loaded")

    # Step 2: Locate username field using By.ID
    print("\n--- Step 2: Interacting with Username using By.ID ---")
    username_field = wait.until(EC.visibility_of_element_located((By.ID, "user-name")))
    username_field.clear()
    username_field.send_keys(VALID_USER)
    assert username_field.get_attribute("value") == VALID_USER
    print(f"[PASS] Username entered using By.ID ('user-name'): {VALID_USER}")

    # Step 3: Locate password field using By.NAME
    print("\n--- Step 3: Interacting with Password using By.NAME ---")
    password_field = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
    password_field.clear()
    password_field.send_keys(VALID_PASS)
    assert password_field.get_attribute("value") == VALID_PASS
    print("[PASS] Password entered using By.NAME ('password'): [MASKED]")
    shot(driver, "02_credentials_entered")

    # Step 4: Locate login button using By.XPATH and click
    print("\n--- Step 4: Interacting with Login Button using By.XPATH ---")
    login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='login-button']"))
    )
    print(f"[PASS] Login button located using By.XPATH: {login_button.get_attribute('value')}")
    login_button.click()

    # Step 5: Validate URL contains /inventory.html
    print("\n--- Step 5: Validating Post-Login URL and Inventory Dashboard ---")
    wait.until(EC.url_contains("/inventory.html"))
    current_url = driver.current_url
    assert "/inventory.html" in current_url, f"Expected '/inventory.html' in URL, but got '{current_url}'"
    print(f"[PASS] URL validation successful: {current_url} contains '/inventory.html'")

    title_elem = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='title']"))
    )
    assert title_elem.text == "Products"
    print(f"[PASS] Dashboard title verified: '{title_elem.text}'")
    shot(driver, "03_inventory_logged_in")


def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    try:
        test_multi_locator_login(driver)
        print("\n==========================================")
        print("[RESULT] Assignment 1 completed successfully!")
        print(f"[RESULT] Screenshots stored in: {SCREENSHOT_DIR}")
        print("==========================================\n")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
