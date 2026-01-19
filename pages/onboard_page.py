from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class OnboardPage(BasePage):
    MAX_PRIVACY_TEXT = (By.XPATH, "//*[contains(@text,'Maximum Privacy')]")
    EASY_SETUP_TEXT = (By.XPATH, "//*[contains(@text,'Easy Setup')]")
    SECURE_ACCOUNTS_TEXT = (By.XPATH, "//*[contains(@text,'Secure All Your Accounts')]")

    CONTINUE_BTN = (By.XPATH, "//*[contains(@text,'Continue')]")
    GET_STARTED_BTN = (By.XPATH, "//*[contains(@text,'Get Started')]")

    def complete_onboarding(self):
        self.wait_for_presence(self.MAX_PRIVACY_TEXT)
        self.wait_and_click(self.CONTINUE_BTN)

        self.wait_for_presence(self.EASY_SETUP_TEXT)
        self.wait_and_click(self.CONTINUE_BTN)

        self.wait_for_presence(self.SECURE_ACCOUNTS_TEXT)
        self.wait_and_click(self.GET_STARTED_BTN)
