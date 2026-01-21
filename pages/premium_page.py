from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class PremiumPage(BasePage):
    MAX_SECURITY_TEXT = (By.XPATH, "//*[contains(@text,'Maximum Security')]")
    SKIP_BTN = (By.XPATH, "//*[contains(@text,'Skip for now')]")

    def skip_if_visible(self):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(self.MAX_SECURITY_TEXT)
            )
        except TimeoutException:
            print("ℹ️ Premium yok")
            return

        self.swipe_until_visible_and_click(self.SKIP_BTN)
