"""
Assignment 4: JavaScript Alerts and Confirms
Site : https://the-internet.herokuapp.com/javascript_alerts  (practice page)
Task : Trigger a JS Alert, a JS Confirm and a JS Prompt.
       - accept the alert
       - dismiss the confirm
       - type into the prompt with driver.switch_to.alert.send_keys(), then submit
Run  : python assignment4_js_alerts.py
       python assignment4_js_alerts.py --pause   (halts while each popup is open so a
                                                  manual screenshot can be taken)
Note : Selenium cannot screenshot a page while a native popup is open, so screenshots
       are taken before and after each popup; popup screenshots are manual (--pause).
"""
import os
import sys
from time import perf_counter

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

URL = "https://the-internet.herokuapp.com/javascript_alerts"
TIMEOUT = 10
SHOT_DIR = "screenshots_a4"
PROMPT_TEXT = "Hello Selenium"
PAUSE = "--pause" in sys.argv


def shot(driver, name):
    os.makedirs(SHOT_DIR, exist_ok=True)
    path = os.path.join(SHOT_DIR, f"{name}.png")
    driver.save_screenshot(path)
    print(f"[SHOT] saved -> {path}")


def pause(message):
    if PAUSE:
        input(f"[PAUSE] {message} Press Enter to continue...")


def click_and_wait_for_alert(driver, wait, css):
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css))).click()
    return wait.until(EC.alert_is_present())


def result_text(driver):
    return driver.find_element(By.ID, "result").text


def test_js_alert(driver, wait):
    alert = click_and_wait_for_alert(driver, wait, "button[onclick='jsAlert()']")
    print(f"[INFO] Alert text : {alert.text}")
    assert alert.text == "I am a JS Alert", f"Unexpected alert text: {alert.text}"
    pause("JS Alert is open. Take a manual screenshot (02_js_alert_popup).")
    driver.switch_to.alert.accept()
    wait.until(EC.text_to_be_present_in_element((By.ID, "result"), "clicked an alert"))
    print(f"[PASS] JS Alert accepted -> result: '{result_text(driver)}'")
    shot(driver, "03_alert_accepted")


def test_js_confirm_dismiss(driver, wait):
    alert = click_and_wait_for_alert(driver, wait, "button[onclick='jsConfirm()']")
    print(f"[INFO] Confirm text: {alert.text}")
    assert alert.text == "I am a JS Confirm", f"Unexpected confirm text: {alert.text}"
    pause("JS Confirm is open. Take a manual screenshot (04_js_confirm_popup).")
    driver.switch_to.alert.dismiss()
    wait.until(EC.text_to_be_present_in_element((By.ID, "result"), "You clicked: Cancel"))
    print(f"[PASS] JS Confirm dismissed -> result: '{result_text(driver)}'")
    shot(driver, "05_confirm_dismissed")


def test_js_confirm_accept(driver, wait):
    click_and_wait_for_alert(driver, wait, "button[onclick='jsConfirm()']")
    driver.switch_to.alert.accept()
    wait.until(EC.text_to_be_present_in_element((By.ID, "result"), "You clicked: Ok"))
    print(f"[PASS] JS Confirm accepted (extra check) -> result: '{result_text(driver)}'")


def test_js_prompt(driver, wait):
    alert = click_and_wait_for_alert(driver, wait, "button[onclick='jsPrompt()']")
    print(f"[INFO] Prompt text : {alert.text}")
    assert alert.text == "I am a JS prompt", f"Unexpected prompt text: {alert.text}"
    driver.switch_to.alert.send_keys(PROMPT_TEXT)
    pause("Text typed into the prompt. Take a manual screenshot (06_js_prompt_popup).")
    driver.switch_to.alert.accept()
    wait.until(EC.text_to_be_present_in_element((By.ID, "result"), f"You entered: {PROMPT_TEXT}"))
    print(f"[PASS] JS Prompt submitted -> result: '{result_text(driver)}'")
    shot(driver, "07_prompt_submitted")


def test_no_alert_timeout(driver):
    """Negative test: alert_is_present must time out when no popup is open."""
    short_wait = WebDriverWait(driver, 2)
    start = perf_counter()
    try:
        short_wait.until(EC.alert_is_present())
        print("[FAIL] Negative test: unexpected alert found")
    except TimeoutException:
        print(f"[PASS] Negative test: TimeoutException after {perf_counter() - start:.2f}s, no alert open")


def main():
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, TIMEOUT)
    try:
        driver.get(URL)
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h3")))
        print(f"[PASS] Page loaded: {driver.title}")
        shot(driver, "01_page_loaded")

        test_js_alert(driver, wait)
        test_js_confirm_dismiss(driver, wait)
        test_js_confirm_accept(driver, wait)
        test_js_prompt(driver, wait)
        test_no_alert_timeout(driver)
        print("[RESULT] Assignment 4 completed")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
