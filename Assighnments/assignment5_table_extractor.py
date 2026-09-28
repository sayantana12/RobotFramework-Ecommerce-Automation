"""
Assignment 5: The HTML Web Table Extractor
Site : https://testautomationpractice.blogspot.com/  (Selenium practice page)
Tables used:
    1. Static Web Table  -> columns: BookName | Author | Subject | Price
    2. Pagination Web Table (table#productTable, rows rendered by JavaScript)
                         -> columns: ID | Name | Price | Select
Task : Iterate through rows and columns, locate a row by matching a name string,
       and return the value from the "Price" column next to it.
Run  : python assignment5_table_extractor.py
       python assignment5_table_extractor.py --product "Smartwatch"
"""
import csv
import os
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

URL = "https://testautomationpractice.blogspot.com/"
TIMEOUT = 15
SHOT_DIR = "screenshots_a5"
CSV_FILE = "extracted_tables.csv"

STATIC_TARGET = "Master In Selenium"          # expected Price: 3000
STATIC_EXPECTED = {"Master In Selenium": "3000", "Learn Java": "500"}
DYNAMIC_TARGET = sys.argv[sys.argv.index("--product") + 1] if "--product" in sys.argv else "Smartwatch"

STATIC_TABLE_XPATH = "//table[.//th[normalize-space()='BookName']]"
DYNAMIC_TABLE_CSS = "table#productTable"


def shot(driver, name):
    os.makedirs(SHOT_DIR, exist_ok=True)
    path = os.path.join(SHOT_DIR, f"{name}.png")
    driver.save_screenshot(path)
    print(f"[SHOT] saved -> {path}")


def highlight(driver, element):
    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});"
        "arguments[0].style.backgroundColor='yellow';", element)


def get_headers(table):
    """Column headers taken from the table itself, so lookups do not depend on column order."""
    return [th.text.strip() for th in table.find_elements(By.XPATH, ".//tr[1]/th")]


def read_rows(table):
    """Iterate through every data row and every column. Returns [(row_element, {header: value})]."""
    headers = get_headers(table)
    result = []
    for row in table.find_elements(By.XPATH, ".//tr[td]"):
        cells = row.find_elements(By.TAG_NAME, "td")
        record = {}
        for col, cell in enumerate(cells):
            key = headers[col] if col < len(headers) and headers[col] else f"col{col + 1}"
            record[key] = cell.text.strip()
        result.append((row, record))
    return result


def find_value(records, name_column, name, value_column):
    """Locate the row whose name_column equals name and return its value_column."""
    for record in records:
        if record.get(name_column) == name:
            return record.get(value_column)
    return None


def print_table(title, headers, records):
    print(f"\n--- {title} ---")
    print(" | ".join(f"{h:<20}" for h in headers))
    for record in records:
        print(" | ".join(f"{record.get(h, ''):<20}" for h in headers))
    print(f"Rows: {len(records)}\n")


def test_static_table(driver, wait, csv_rows):
    table = wait.until(EC.visibility_of_element_located((By.XPATH, STATIC_TABLE_XPATH)))
    headers = get_headers(table)
    pairs = read_rows(table)
    records = [rec for _, rec in pairs]
    print_table("Static Web Table", headers, records)
    csv_rows.extend(["static"] + [rec.get(h, "") for h in headers] for rec in records)

    for name, expected in STATIC_EXPECTED.items():
        price = find_value(records, "BookName", name, "Price")
        assert price == expected, f"{name}: expected {expected}, got {price}"
        print(f"[PASS] Static table: Price of '{name}' = {price}")

    for row, rec in pairs:
        if rec.get("BookName") == STATIC_TARGET:
            highlight(driver, row)
    shot(driver, "01_static_table_row_highlighted")


def read_current_page(driver, wait):
    table = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, DYNAMIC_TABLE_CSS)))
    wait.until(lambda d: len(table.find_elements(By.CSS_SELECTOR, "tbody tr")) > 0)
    return table, read_rows(table)


def test_dynamic_table(driver, wait, csv_rows):
    table, pairs = read_current_page(driver, wait)
    headers = get_headers(table)
    print(f"[INFO] Dynamic table headers: {headers}")
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", table)
    shot(driver, "02_dynamic_table_page1")

    page_count = len(driver.find_elements(By.CSS_SELECTOR, "#pagination li a"))
    print(f"[INFO] Pagination links found: {page_count}")
    all_records, found_price, found_on_page = [], None, None

    for page in range(1, page_count + 1):
        if page > 1:
            first_row = table.find_element(By.CSS_SELECTOR, "tbody tr")
            link = wait.until(lambda d: next(
                (a for a in d.find_elements(By.CSS_SELECTOR, "#pagination li a")
                 if a.text.strip() == str(page) and a.is_displayed()), None))
            link.click()
            wait.until(EC.staleness_of(first_row))          # old rows replaced by new rows
            table, pairs = read_current_page(driver, wait)

        for row, rec in pairs:
            all_records.append(rec)
            if rec.get("Name") == DYNAMIC_TARGET and found_price is None:
                found_price, found_on_page = rec.get("Price"), page
                highlight(driver, row)
                shot(driver, "03_dynamic_target_row_highlighted")
        print(f"[INFO] Page {page}: {len(pairs)} rows read")

    print_table("Dynamic (Pagination) Web Table, all pages", ["ID", "Name", "Price"], all_records)
    csv_rows.extend(["dynamic", r.get("ID", ""), r.get("Name", ""), r.get("Price", ""), ""]
                    for r in all_records)

    if found_price is None:
        names = ", ".join(r.get("Name", "") for r in all_records)
        raise LookupError(f"'{DYNAMIC_TARGET}' not found. Available names: {names}. "
                          f"Re-run with --product \"<name>\".")
    print(f"[PASS] Dynamic table: Price of '{DYNAMIC_TARGET}' = {found_price} (found on page {found_on_page})")


def main():
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, TIMEOUT)
    csv_rows = []
    try:
        driver.get(URL)
        wait.until(EC.title_contains("Automation Testing Practice"))
        print(f"[PASS] Page loaded: {driver.title}")
        test_static_table(driver, wait, csv_rows)
        test_dynamic_table(driver, wait, csv_rows)

        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["table", "col1", "col2", "col3", "col4"])
            writer.writerows(csv_rows)
        print(f"[PASS] Extracted data written to {CSV_FILE} ({len(csv_rows)} rows)")
        print("[RESULT] Assignment 5 completed")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
