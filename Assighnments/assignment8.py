from pathlib import Path

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "https://www.saucedemo.com/"
DATA_FILE = Path(__file__).resolve().parent / "login_test_data.csv"
SCREENSHOT_DIR = Path(__file__).resolve().parent / "screenshot_a8"
TIMEOUT = 10

SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


def save_screenshot(driver, filename: str) -> None:
    path = SCREENSHOT_DIR / filename
    driver.save_screenshot(str(path))
    print(f"[SHOT] saved -> {path}")


def login_and_validate(driver, wait, row) -> bool:
    case_id = row["case_id"]
    username = row["username"]
    password = row["password"]
    expected = row["expected_message"]
    expected_type = row["expected_type"]
    description = row["description"]

    driver.get(BASE_URL)

    wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).clear()
    driver.find_element(By.ID, "user-name").send_keys(username)

    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys(password)

    wait.until(EC.element_to_be_clickable((By.ID, "login-button"))).click()

    screenshot_name = f"{case_id}_{description}.png"

    if expected_type == "success":
        wait.until(EC.url_contains("inventory.html"))
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='title']")))
        title = driver.find_element(By.CSS_SELECTOR, "[data-test='title']").text
        assert title == expected
        save_screenshot(driver, screenshot_name)
        print(f"[PASS] {case_id}: successful login -> {title}")
        return True

    error = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']")))
    wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "[data-test='error']"), expected))
    actual = error.text
    assert expected in actual, f"Expected '{expected}' in error, got '{actual}'"
    save_screenshot(driver, screenshot_name)
    print(f"[PASS] {case_id}: validation error displayed -> {actual}")
    return True


def main():
    data = pd.read_csv(DATA_FILE).fillna("")

    required_columns = {
        "case_id",
        "username",
        "password",
        "expected_message",
        "expected_type",
        "description",
    }
    missing = required_columns - set(data.columns)
    if missing:
        raise ValueError(f"Missing CSV columns: {sorted(missing)}")

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    passed = 0
    failed = 0

    print(f"Loaded {len(data)} test cases from {DATA_FILE.name}")

    for _, row in data.iterrows():
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, TIMEOUT)
        try:
            login_and_validate(driver, wait, row)
            passed += 1
        except (AssertionError, TimeoutException, Exception) as exc:
            failed += 1
            print(f"[FAIL] {row['case_id']}: {exc}")
            failure_name = f"{row['case_id']}_failure.png"
            save_screenshot(driver, failure_name)
        finally:
            driver.quit()

    print("\n[RESULT] Assignment 8 completed")
    print(f"[RESULT] Total cases : {len(data)}")
    print(f"[RESULT] Passed      : {passed}")
    print(f"[RESULT] Failed      : {failed}")
    print(f"[RESULT] Screenshots: {SCREENSHOT_DIR}")

    if failed:
        raise AssertionError(f"{failed} data-driven test case(s) failed")


if __name__ == "__main__":
    main()
