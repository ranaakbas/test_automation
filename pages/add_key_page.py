from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class AddKeyPage(BasePage):
    WEBSITE_INPUT = (By.XPATH, "//android.widget.EditText[@text='Enter website name']")
    ACCOUNT_INPUT = (By.XPATH, "//android.widget.EditText[@text='user@example.com']")
    KEY_INPUT = (By.XPATH, "//android.widget.EditText[@text='_ _ _  _ _ _  _ _ _']")
    ADD_KEY_BTN = (AppiumBy.ACCESSIBILITY_ID, "Add Key")

    def fill_key_form(self, website, account, key):
        self.send_keys_human(self.WEBSITE_INPUT, website)
        self.send_keys_human(self.ACCOUNT_INPUT, account)
        self.send_keys_human(self.KEY_INPUT, key)

    def submit(self):
        self.wait_and_click(self.ADD_KEY_BTN)
