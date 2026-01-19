from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class PremiumPage(BasePage):
    MAX_SECURITY_TEXT = (By.XPATH, "//*[contains(@text,'Maximum Security')]")
    SKIP_BTN = (By.XPATH, "//*[contains(@text,'Skip for now')]")

    def skip_if_visible(self):
        self.wait_for_visible(self.MAX_SECURITY_TEXT)
        skip_btn = self.find_element_with_swipe(self.SKIP_BTN)
        skip_btn.click()
