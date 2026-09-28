"""
Assignment 3: Dynamic Dropdowns & Checkboxes
Site       : https://testautomationpractice.blogspot.com/ (Automation Practice Page)
Focus      : Mastering element identification, synchronization, and basic browser actions.
Task       : Open a registration/practice form containing:
             1. Multiple checkboxes (Days of the week).
             2. Search-as-you-type autocomplete dynamic dropdown (comboBox + dropdown suggestions).
             3. Standard select dropdown (Country selection).
Task Steps :
             - Select specific checkboxes (e.g., Monday, Wednesday, Friday).
             - Verify their state using .is_selected() (assert selected == True and unselected == False).
             - Type query into the autocomplete dropdown.
             - Loop through the suggested results dynamically to locate and select the matching option.
             - Verify the selected value in the combobox input.
Run        : python assignment3_dropdowns_checkboxes.py
"""

from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://testautomationpractice.blogspot.com/"
TIMEOUT = 15
SCREENSHOT_DIR = Path(__file__).resolve().parent / "screenshot_a3"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

DAYS_TO_SELECT = ["monday", "wednesday", "friday"]
DAYS_TO_LEAVE_UNSELECTED = ["sunday", "tuesday", "thursday", "saturday"]
SEARCH_ITEM = "Item 15"
SELECTED_COUNTRY = "canada"


def shot(driver, name: str) -> Path:
    path = SCREENSHOT_DIR / f"{name}.png"
    driver.save_screenshot(str(path))
    print(f"[SHOT] saved -> {path}")
    return path


def scroll_to_element(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'instant'});", element)


def test_checkboxes(driver, wait):
    print("\n--- Part 1: Multiple Checkboxes Selection & Verification ---")
    wait.until(EC.presence_of_element_located((By.ID, "monday")))

    # Step 1: Select target checkboxes and verify state
    for day in DAYS_TO_SELECT:
        checkbox = wait.until(EC.presence_of_element_located((By.ID, day)))
        scroll_to_element(driver, checkbox)

        if not checkbox.is_selected():
            wait.until(EC.element_to_be_clickable((By.ID, day))).click()

        assert checkbox.is_selected() is True, f"Expected checkbox '{day}' to be selected!"
        print(f"[PASS] Checkbox '{day}' successfully selected (.is_selected() == True)")

    # Step 2: Verify unselected checkboxes
    for day in DAYS_TO_LEAVE_UNSELECTED:
        checkbox = driver.find_element(By.ID, day)
        assert checkbox.is_selected() is False, f"Expected checkbox '{day}' to be unselected!"
        print(f"[PASS] Unselected checkbox '{day}' verified (.is_selected() == False)")

    shot(driver, "01_checkboxes_selected")


def test_dynamic_autocomplete_dropdown(driver, wait):
    print("\n--- Part 2: Search-as-you-type Autocomplete Dropdown ---")
    combobox = wait.until(EC.visibility_of_element_located((By.ID, "comboBox")))
    scroll_to_element(driver, combobox)

    # Type search term
    combobox.clear()
    combobox.send_keys("Item")
    print(f"[INFO] Typed query 'Item' into autocomplete input #comboBox")

    # Wait for suggestions container to become visible
    dropdown_container = wait.until(EC.visibility_of_element_located((By.ID, "dropdown")))
    shot(driver, "02_autocomplete_suggestions_opened")

    # Loop through suggestions dynamically to locate and click matching option
    suggestions = wait.until(
        lambda d: d.find_elements(By.XPATH, "//div[@id='dropdown']//div | //div[@id='dropdown']/*")
    )
    print(f"[INFO] Discovered {len(suggestions)} suggestion elements in dynamic dropdown")

    matched = False
    for option in suggestions:
        text = option.text.strip()
        if text == SEARCH_ITEM:
            scroll_to_element(driver, option)
            option.click()
            matched = True
            print(f"[PASS] Found and clicked matching option: '{SEARCH_ITEM}'")
            break

    assert matched, f"Could not find matching suggestion '{SEARCH_ITEM}' in dropdown options!"

    # Verify input field now displays the selected value
    actual_value = combobox.get_attribute("value").strip()
    assert actual_value == SEARCH_ITEM, f"Expected '{SEARCH_ITEM}' in #comboBox, got '{actual_value}'"
    print(f"[PASS] Autocomplete dropdown value verified: '{actual_value}'")
    shot(driver, "03_autocomplete_option_selected")


def test_standard_select_dropdown(driver, wait):
    print("\n--- Part 3: Standard Select Dropdown (Country) ---")
    country_elem = wait.until(EC.presence_of_element_located((By.ID, "country")))
    scroll_to_element(driver, country_elem)

    select = Select(country_elem)
    select.select_by_value(SELECTED_COUNTRY)

    selected_option = select.first_selected_option
    assert selected_option.get_attribute("value") == SELECTED_COUNTRY
    print(f"[PASS] Country select dropdown verified: '{selected_option.text}' (value={SELECTED_COUNTRY})")
    shot(driver, "04_country_dropdown_selected")


def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, TIMEOUT)

    try:
        print("\n--- Navigating to Test Automation Practice Page ---")
        driver.get(BASE_URL)
        wait.until(EC.title_contains("Automation Testing Practice"))
        print(f"[PASS] Page loaded: {driver.title}")

        test_checkboxes(driver, wait)
        test_dynamic_autocomplete_dropdown(driver, wait)
        test_standard_select_dropdown(driver, wait)

        print("\n==========================================")
        print("[RESULT] Assignment 3 completed successfully!")
        print(f"[RESULT] Screenshots stored in: {SCREENSHOT_DIR}")
        print("==========================================\n")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
