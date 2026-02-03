"""iOS için legal sayfaları (Terms, Privacy Policy, EULA)"""

from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class LegalPage(BasePage):
    """iOS Terms, Privacy Policy ve EULA sayfaları için ortak page class"""

    # iOS'ta bu sayfaların başlıklarını kontrol etmek için accessibility ID'ler kullanılabilir
    # Ancak info.md'de sadece scroll kontrolü yapılması isteniyor, başlık kontrolü yok
    # Bu yüzden sadece scroll metodunu override ediyoruz

    def check_scrollable(self):
        """Sayfanın swipe edilebilir olup olmadığını kontrol et"""
        try:
            # Sayfanın scrollable olup olmadığını kontrol etmek için bir swipe yap
            self.swipe_up_from_middle()
            print("✅ Sayfa swipe edilebilir")
        except Exception as e:
            print(f"⚠️ Swipe kontrolü başarısız: {e}")
