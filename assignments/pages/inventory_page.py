from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InventoryPage:
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    PAGE_TITLE = (By.CSS_SELECTOR, ".title")
    FIRST_PRODUCT = (By.CSS_SELECTOR, ".inventory_item_name")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def is_loaded(self):
        self.wait.until(EC.visibility_of_element_located(self.INVENTORY_CONTAINER))
        return self.driver.find_element(*self.PAGE_TITLE).text == "Products"

    def get_first_product_name(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.FIRST_PRODUCT)
        ).text

    def logout(self):
        self.wait.until(EC.element_to_be_clickable(self.MENU_BUTTON)).click()
        logout_link = self.wait.until(EC.visibility_of_element_located(self.LOGOUT_LINK))
        self.driver.execute_script("arguments[0].click();", logout_link)
