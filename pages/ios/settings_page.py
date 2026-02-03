"""iOS için Settings sayfası"""

from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class SettingsPage(BasePage):
    """iOS Settings sayfası"""

    # ===== SETTINGS BUTTONS =====
    PREMIUM_BANNER = (
        AppiumBy.ACCESSIBILITY_ID,
        "Maximum Security! Activate enhanced security with an Authenticator for full 2FA protection.",
    )

    TERMS_OF_SERVICE_BTN = (AppiumBy.ACCESSIBILITY_ID, "Terms of Service")
    PRIVACY_POLICY_BTN = (AppiumBy.ACCESSIBILITY_ID, "Privacy Policy")
    EULA_BTN = (AppiumBy.ACCESSIBILITY_ID, "EULA")

    BACK_BTN = (AppiumBy.ACCESSIBILITY_ID, "Back")

    # ===== ACTIONS =====

    def click_premium_banner(self):
        """Settings ekranındaki premium banner'a tıkla"""
        self.wait_and_click(self.PREMIUM_BANNER)
        print("✅ Settings'te premium banner'a tıklandı")

    def click_terms_of_service(self):
        """Terms of Service ekranını aç"""
        self.wait_and_click(self.TERMS_OF_SERVICE_BTN)
        print("✅ Terms of Service ekranı açıldı")

    def click_privacy_policy(self):
        """Privacy Policy ekranını aç"""
        self.wait_and_click(self.PRIVACY_POLICY_BTN)
        print("✅ Privacy Policy ekranı açıldı")

    def click_eula(self):
        """EULA ekranını aç"""
        self.wait_and_click(self.EULA_BTN)
        print("✅ EULA ekranı açıldı")

    # ===== BACK ACTIONS =====

    def click_back_from_document(self):
        """
        Terms of Service / Privacy Policy / EULA
        ekranlarından geri dönmek için kullanılır.
        Inspector'da ayrışmayan custom back ikonu
        koordinat bazlı tap ile kapatılır.
        """
        self._tap_back_icon_by_coordinate()
        print("✅ Document ekranından geri dönüldü (coordinate tap)")

    def click_back_to_home(self):
        """Settings ekranından homepage'e geri dön"""
        self.wait_and_click(self.BACK_BTN)
        print("✅ Settings'ten homepage'e geri dönüldü")

    # ===== HELPERS =====

    def _tap_back_icon_by_coordinate(self):
        """
        iOS custom header içindeki back ikonu için
        oransal koordinatla tap eder.
        """
        size = self.driver.get_window_size()

        x = int(size["width"] * 0.08)  # sol kenar
        y = int(size["height"] * 0.12)  # status bar altı

        self.driver.execute_script("mobile: tap", {"x": x, "y": y})
