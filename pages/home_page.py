from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class HomePage(BasePage):
    ENTER_MANUALLY_BTN = (AppiumBy.ACCESSIBILITY_ID, "Enter Manually")

    def go_to_add_key(self):
        self.wait_and_click(self.ENTER_MANUALLY_BTN)
