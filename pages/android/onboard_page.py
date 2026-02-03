from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage


class OnboardPage(BasePage):
    MAX_PRIVACY_TEXT = (By.XPATH, "//*[contains(@text,'Maximum Privacy')]")
    EASY_SETUP_TEXT = (By.XPATH, "//*[contains(@text,'Easy Setup')]")
    SECURE_ACCOUNTS_TEXT = (By.XPATH, "//*[contains(@text,'Secure All Your Accounts')]")

    CONTINUE_BTN = (By.XPATH, "//*[contains(@text,'Continue')]")
    GET_STARTED_BTN = (By.XPATH, "//*[contains(@text,'Get Started')]")

    def complete_onboarding(self):
        self.wait_for_visible(self.MAX_PRIVACY_TEXT)
        self.wait_and_click(self.CONTINUE_BTN)

        self.wait_for_visible(self.EASY_SETUP_TEXT)
        self.wait_and_click(self.CONTINUE_BTN)

        # Son sayfada GET_STARTED_BTN'ı bul ve tıkla
        # Önce normal bekleme dene, başarısız olursa swipe ile ara
        try:
            self.wait_for_visible(self.SECURE_ACCOUNTS_TEXT)
            self.wait_and_click(self.GET_STARTED_BTN)
        except TimeoutException:
            # Text bulunamazsa direkt butonu swipe ile ara
            print(
                "⚠️ SECURE_ACCOUNTS_TEXT bulunamadı, GET_STARTED_BTN swipe ile aranıyor..."
            )
            self.swipe_until_visible_and_click(self.GET_STARTED_BTN)
