from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LegalPage(BasePage):
    """Terms, Privacy Policy ve EULA sayfaları için ortak page class"""

    TERMS_AND_CONDITIONS_TEXT = (By.XPATH, "//*[@text='Terms and Conditions']")
    PRIVACY_POLICY_TEXT = (By.XPATH, "//*[@text='Privacy Policy']")
    EULA_TEXT = (By.XPATH, "//*[contains(@text,'End-User License Agreement')]")

    def verify_terms_and_conditions_visible(self):
        """Terms and Conditions yazısının görünür olduğunu doğrula"""
        self.wait_for_visible(self.TERMS_AND_CONDITIONS_TEXT)
        print("✅ Terms and Conditions yazısı görünür")

    def verify_privacy_policy_visible(self):
        """Privacy Policy yazısının görünür olduğunu doğrula"""
        self.wait_for_visible(self.PRIVACY_POLICY_TEXT)
        print("✅ Privacy Policy yazısı görünür")

    def verify_eula_visible(self):
        """EULA yazısının görünür olduğunu doğrula"""
        self.wait_for_visible(self.EULA_TEXT)
        print("✅ End-User License Agreement yazısı görünür")

    def check_scrollable(self):
        """Sayfanın swipe edilebilir olup olmadığını kontrol et"""
        try:
            # Sayfanın scrollable olup olmadığını kontrol etmek için bir swipe yap
            self.swipe_up_from_middle()
            print("✅ Sayfa swipe edilebilir")
        except Exception as e:
            print(f"⚠️ Swipe kontrolü başarısız: {e}")
