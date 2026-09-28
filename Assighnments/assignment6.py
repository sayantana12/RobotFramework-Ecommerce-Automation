from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


URL = "https://www.selenium.dev/selenium/web/window_switching_tests/page_with_frame.html"

# All Assignment 6 screenshots go into this folder.
# The folder is created automatically if it does not exist.
SCREENSHOT_DIR = Path(__file__).resolve().parent / "screenshot_a6"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


def test_windows_tabs_and_iframe():

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    try:
        # -------------------------------------------------
        # 1. Open main page
        # -------------------------------------------------
        print("\nOpening main page...")

        driver.get(URL)

        main_window = driver.current_window_handle

        print("Main window handle:", main_window)

        driver.save_screenshot(
            str(SCREENSHOT_DIR / "01_main_page.png")
        )

        # -------------------------------------------------
        # 2. Switch to iframe
        # -------------------------------------------------
        print("Switching to iframe...")

        wait.until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.NAME, "myframe")
            )
        )

        print("Successfully switched to iframe")

        # -------------------------------------------------
        # 3. Read iframe content
        # -------------------------------------------------
        frame_body = wait.until(
            EC.presence_of_element_located(
                (By.TAG_NAME, "body")
            )
        )

        frame_text = frame_body.text.strip()

        print("Iframe content:")
        print(frame_text)

        assert "Simple page with simple test." in frame_text

        driver.save_screenshot(
            str(SCREENSHOT_DIR / "02_inside_iframe.png")
        )

        # -------------------------------------------------
        # 4. Return to main document
        # -------------------------------------------------
        print("Returning to main document...")

        driver.switch_to.default_content()

        wait.until(
            EC.presence_of_element_located(
                (By.ID, "a-link-that-opens-a-new-window")
            )
        )

        driver.save_screenshot(
            str(SCREENSHOT_DIR / "03_main_document.png")
        )

        # -------------------------------------------------
        # 5. Store current window handles
        # -------------------------------------------------
        existing_windows = set(driver.window_handles)

        print("Existing windows:", existing_windows)

        # -------------------------------------------------
        # 6. Open new tab/window
        # -------------------------------------------------
        print("Opening new tab/window...")

        wait.until(
            EC.element_to_be_clickable(
                (By.ID, "a-link-that-opens-a-new-window")
            )
        ).click()

        # -------------------------------------------------
        # 7. Wait for new window
        # -------------------------------------------------
        wait.until(
            EC.new_window_is_opened(existing_windows)
        )

        new_windows = set(driver.window_handles) - existing_windows
        new_window = new_windows.pop()

        driver.switch_to.window(new_window)

        print("Switched to new tab/window")

        # -------------------------------------------------
        # 8. Verify title
        # -------------------------------------------------
        wait.until(
            lambda d: d.title == "Simple Page"
        )

        print("New tab title:", driver.title)

        assert driver.title == "Simple Page"

        driver.save_screenshot(
            str(SCREENSHOT_DIR / "04_new_tab.png")
        )

        # -------------------------------------------------
        # 9. Close new tab
        # -------------------------------------------------
        print("Closing new tab...")

        driver.close()

        # -------------------------------------------------
        # 10. Return to main window
        # -------------------------------------------------
        print("Switching back to main window...")

        driver.switch_to.window(main_window)

        print("Current window:", driver.current_window_handle)

        assert driver.current_window_handle == main_window

        wait.until(
            EC.presence_of_element_located(
                (By.ID, "a-link-that-opens-a-new-window")
            )
        )

        driver.save_screenshot(
            str(SCREENSHOT_DIR / "05_main_window_restored.png")
        )

        print("\nAssignment completed successfully.")
        print("Screenshots saved in:")
        print(SCREENSHOT_DIR)

    finally:
        driver.quit()


if __name__ == "__main__":
    test_windows_tabs_and_iframe()