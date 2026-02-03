"""iOS için premium sayfası - accessibility ID ile Maximum Security, Skip for now."""

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.android.premium_page import PremiumPage as AndroidPremiumPage


class PremiumPage(AndroidPremiumPage):
    """iOS premium - accessibility ID locator'ları. Diğer aksiyonlar base PremiumPage'den."""

    MAX_SECURITY_TEXT = (AppiumBy.ACCESSIBILITY_ID, "Maximum Security")
    SKIP_BTN = (AppiumBy.ACCESSIBILITY_ID, "Skip for now")
    PREMIUM_BANNER = (AppiumBy.ACCESSIBILITY_ID, "Maximum Security")
    # iOS'ta Back ikonu - uygulama yapısına göre güncellenebilir
    BACK_ICON = (AppiumBy.ACCESSIBILITY_ID, "Back")

    def skip_if_visible(self):
        """
        Premium paywall görünürse: Maximum Security'yi gör, aşağı kaydır,
        Skip for now'u ekranda görünür yap ve tıkla.
        """
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.MAX_SECURITY_TEXT)
            )
            print("📱 iOS Premium paywall tespit edildi")
        except TimeoutException:
            print("ℹ️ Premium sayfası yok")
            return

        result = self.swipe_until_visible_and_click(
            self.SKIP_BTN, max_swipe=15, min_swipe=5
        )
        if result:
            print("✅ Premium sayfası geçildi (Skip for now)")
            self._pause(1.0, 1.5)
        else:
            print("⚠️ Skip for now butonu tıklanamadı")
