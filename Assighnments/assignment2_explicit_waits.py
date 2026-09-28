"""
Assignment 2: Synchronization & Explicit Waits
Site   : https://tutorialsninja.com/demo/  (OpenCart demo store)
Dynamic content used:
    1. Search results loaded after a page request
    2. AJAX "Add to Cart" success alert (appears only after the server responds)
    3. AJAX-refreshed cart total (#cart-total) and cart dropdown (#cart ul.dropdown-menu)
Constraint: no fixed delays and no implicit wait. Only WebDriverWait + expected_conditions.
Run: python assignment2_explicit_waits.py
"""
import os
from time import perf_counter

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "https://tutorialsninja.com/demo/"
PRODUCT = "iMac"
TIMEOUT = 15
SHOT_DIR = "screenshots"


def shot(driver, name):
    os.makedirs(SHOT_DIR, exist_ok=True)
    path = os.path.join(SHOT_DIR, f"{name}.png")
    driver.save_screenshot(path)
    print(f"[SHOT] saved -> {path}")


def test_dynamic_content_waits(driver):
    wait = WebDriverWait(driver, TIMEOUT)

    # Step 1: page load synchronization
    driver.get(BASE_URL)
    wait.until(EC.title_contains("Your Store"))
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#logo")))
    print("[PASS] Step 1: home page loaded, title and logo visible")
    shot(driver, "01_home_loaded")

    # Step 2: search and wait for results
    search_box = wait.until(EC.element_to_be_clickable((By.NAME, "search")))
    search_box.clear()
    search_box.send_keys(PRODUCT)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#search button"))).click()
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-layout")))
    wait.until(EC.visibility_of_element_located((By.LINK_TEXT, PRODUCT)))
    print(f"[PASS] Step 2: search results for '{PRODUCT}' displayed")
    shot(driver, "02_search_results")

    # Step 3: trigger AJAX call and wait for the dynamic success alert
    add_btn = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, ".product-layout button[onclick^='cart.add']")))
    start = perf_counter()
    add_btn.click()
    alert = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "div.alert-success")))
    elapsed = perf_counter() - start
    assert "Success: You have added" in alert.text, f"Unexpected alert text: {alert.text}"
    print(f"[PASS] Step 3: AJAX alert visible after {elapsed:.2f}s -> {alert.text.splitlines()[0]}")
    shot(driver, "03_ajax_alert_visible")

    # Step 4: wait for the cart total text to refresh
    start = perf_counter()
    wait.until(EC.text_to_be_present_in_element((By.ID, "cart-total"), "1 item(s)"))
    elapsed = perf_counter() - start
    print(f"[PASS] Step 4: cart total updated to '{driver.find_element(By.ID, 'cart-total').text}' "
          f"(extra wait {elapsed:.2f}s)")
    shot(driver, "04_cart_total_updated")

    # Step 5: dismiss alert and wait until it disappears
    alert.find_element(By.CSS_SELECTOR, "button.close").click()
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.alert-success")))
    print("[PASS] Step 5: alert dismissed, no longer visible")

    # Step 6: open cart dropdown and wait for its AJAX-loaded content
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#cart > button"))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#cart ul.dropdown-menu")))
    wait.until(EC.text_to_be_present_in_element(
        (By.CSS_SELECTOR, "#cart ul.dropdown-menu"), PRODUCT))
    print(f"[PASS] Step 6: cart dropdown loaded and lists '{PRODUCT}'")
    shot(driver, "05_cart_dropdown_loaded")


def test_timeout_behaviour(driver):
    """Negative test: an element that never appears must raise TimeoutException."""
    short_wait = WebDriverWait(driver, 3)
    start = perf_counter()
    try:
        short_wait.until(EC.visibility_of_element_located((By.ID, "non-existent-loader")))
        print("[FAIL] Negative test: element unexpectedly found")
    except TimeoutException:
        elapsed = perf_counter() - start
        print(f"[PASS] Negative test: TimeoutException raised after {elapsed:.2f}s (limit 3s)")


def main():
    driver = webdriver.Chrome()
    driver.maximize_window()
    try:
        test_dynamic_content_waits(driver)
        test_timeout_behaviour(driver)
        print("[RESULT] Assignment 2 completed")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
