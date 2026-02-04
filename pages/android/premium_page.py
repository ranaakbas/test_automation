from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class PremiumPage(BasePage):
    MAX_SECURITY_TEXT = (By.XPATH, "//*[contains(@text,'Maximum Security')]")
    SKIP_BTN = (By.XPATH, "//*[contains(@text,'Skip for now')]")
    PREMIUM_BANNER = (
        By.XPATH,
        '//android.view.ViewGroup[@content-desc="Maximum Security!, Activate enhanced security with an Authenticator for full 2FA protection."]/android.view.ViewGroup[1]',
    )
    TERMS_OF_SERVICE_BTN = (AppiumBy.ACCESSIBILITY_ID, "Terms of Service")
    PRIVACY_POLICY_BTN = (AppiumBy.ACCESSIBILITY_ID, "Privacy Policy")
    EULA_BTN = (AppiumBy.ACCESSIBILITY_ID, "EULA")
    CONTACT_US_BTN = (AppiumBy.ACCESSIBILITY_ID, "Contact Us")
    BACK_ICON = (By.XPATH, "//com.horcrux.svg.SvgView")
    BACK_BTN = (AppiumBy.ACCESSIBILITY_ID, "Back")

    def wait_until_premium_actions_visible(self, timeout_s=10):
        """
        Premium ekranına (legal aksiyonlar) geri dönüldüğünü doğrular.
        Contact Us / Terms gibi butonlar görünmeden "geri" aksiyonu yapmayız;
        aksi halde yanlış ekranda (örn. Settings) back basıp homepage'e düşebiliyor.
        """
        return WebDriverWait(self.driver, timeout_s).until(
            EC.visibility_of_element_located(self.CONTACT_US_BTN)
        )

    def verify_premium_upsell_visible(self, timeout_s=10):
        """
        Premium upsell ekranının (Maximum Security metni) gerçekten geldiğini
        doğrular. Bu sayede Jenkins tarafında da bu ekranın açılmaması durumunda
        testler açıkça FAIL olur.
        """
        WebDriverWait(self.driver, timeout_s).until(
            EC.visibility_of_element_located(self.MAX_SECURITY_TEXT)
        )
        print("✅ Premium upsell ekranı görünür")

    def skip_if_visible(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.MAX_SECURITY_TEXT)
            )
            print("📱 Premium sayfası tespit edildi")
        except TimeoutException:
            print("ℹ️ Premium yok")
            return

        result = self.swipe_until_visible_and_click(
            self.SKIP_BTN, max_swipe=15, min_swipe=5
        )
        if result:
            print("✅ Premium sayfası geçildi")
            self._pause(1.0, 1.5)  # Sayfa geçişi için bekle
        else:
            print("⚠️ Skip butonu tıklanamadı")

    def click_premium_banner(self):
        """
        Premium banner'a tıkla.

        Jenkins / farklı ekran boyutlarında banner bazen ilk ekranda olmayıp
        aşağıda kalabiliyor. Bu nedenle, Skip butonunda yaptığımız gibi
        swipe ile arayıp tıklamayı deniyoruz.
        """
        result = self.swipe_until_visible_and_click(
            self.PREMIUM_BANNER,
            max_swipe=10,
            min_swipe=0,
        )

        if result:
            print("✅ Premium banner'a tıklandı")
        else:
            print("❌ Premium banner bulunamadı veya tıklanamadı")
            raise TimeoutException("Premium banner bulunamadı veya tıklanamadı")

    def click_terms_of_service(self):
        """Terms of Service butonuna tıkla"""
        self.wait_and_click(self.TERMS_OF_SERVICE_BTN)
        print("✅ Terms of Service butonuna tıklandı")

    def click_privacy_policy(self):
        """Privacy Policy butonuna tıkla"""
        self.wait_and_click(self.PRIVACY_POLICY_BTN)
        print("✅ Privacy Policy butonuna tıklandı")

    def click_eula(self):
        """EULA butonuna tıkla"""
        self.wait_and_click(self.EULA_BTN)
        print("✅ EULA butonuna tıklandı")

    def click_contact_us(self):
        """Contact Us butonuna tıkla"""
        self.wait_and_click(self.CONTACT_US_BTN)
        print("✅ Contact Us butonuna tıklandı")

    def click_back_icon(self):
        """Back ikonuna tıkla"""
        self.wait_and_click(self.BACK_ICON)
        print("✅ Back ikonuna tıklandı")

    def click_back_button(self):
        """
        Back butonuna tıkla (content-desc: Back).

        Not: Eskiden bulunamazsa direkt telefon back'ine basıyorduk; bu bazı cihazlarda
        Settings gibi ara ekranda çalışıp homepage'e düşebiliyor. Bu yüzden önce
        premium aksiyonlarının görünür olduğundan emin olup, in-app back'i zorlarız.
        """
        try:
            self.wait_until_premium_actions_visible(timeout_s=10)
        except TimeoutException:
            # Premium aksiyonları görünmüyorsa, burada agresif "driver.back()" yapmıyoruz.
            # Yine de testlerin tamamen kilitlenmemesi için son çare olarak bir kez back.
            print("⚠️ Premium aksiyonları görünmedi, son çare: telefon geri tuşu (1x)")
            self.press_back_button()

        # Önce Back (accessibility id) dene, olmazsa back ikonunu dene.
        try:
            WebDriverWait(self.driver, 8).until(
                EC.element_to_be_clickable(self.BACK_BTN)
            ).click()
            self._pause(0.4, 0.8)
            print("✅ Back butonuna tıklandı")
            return
        except TimeoutException:
            pass

        try:
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.BACK_ICON)
            ).click()
            self._pause(0.4, 0.8)
            print("✅ Back ikonuna tıklandı")
            return
        except TimeoutException:
            print("⚠️ Back UI bulunamadı, son çare: telefon geri tuşu (1x)")
            self.press_back_button()
            print("✅ Telefon geri tuşu ile geri dönüldü")
