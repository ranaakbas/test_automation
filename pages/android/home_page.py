from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage


class HomePage(BasePage):
    ENTER_MANUALLY_BTN = (AppiumBy.ACCESSIBILITY_ID, "Enter Manually")
    SCAN_QR_CODE_BTN = (AppiumBy.ACCESSIBILITY_ID, "Scan Qr Code")
    PREMIUM_PAGE_BTN = (By.XPATH, "//com.horcrux.svg.RectView")
    TOP_RIGHT_BUTTON = (
        By.XPATH,
        "//android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup[2]/com.horcrux.svg.SvgView",
    )

    def go_to_add_key(self):
        self.wait_for_visible(self.ENTER_MANUALLY_BTN)
        self.wait_and_click(self.ENTER_MANUALLY_BTN)

        """
        Sağ üstteki butonun gerçekten görünür olduğunu doğrular.
        Görünmezse TimeoutException ile testi FAIL eder.
        """
        self.wait_for_visible(self.TOP_RIGHT_BUTTON, timeout=timeout_s)
        print("✅ Sağ üstteki buton (TOP_RIGHT_BUTTON) görünür")

    def click_top_right_button(self):
        self.wait_and_click(self.TOP_RIGHT_BUTTON)

    def verify_enter_manually_visible(self):
        """
        Enter Manually butonunun görünür olduğunu doğrula.

        Jenkins / uzak cihazlarda bazen akış ara bir ekranda (ör. Settings/Add Key)
        kalabiliyor. Bu durumda önce normal şekilde bekleriz; başarısız olursa
        tek seferlik telefon geri tuşuna basıp tekrar deneriz.
        """
        try:
            self.wait_for_visible(self.ENTER_MANUALLY_BTN)
            print("✅ Enter Manually butonu görünür")
            return
        except TimeoutException:
            print(
                "ℹ️ Enter Manually butonu ilk denemede görünmedi, "
                "geri tuşu ile homepage'e dönmeyi deniyoruz"
            )

        # Ara ekrandan (ör. Add Key / Settings) tek seferlik geri dönmeyi dene
        self.press_back_button()

        # Geri sonrası tekrar dene; hala bulunamazsa orijinal TimeoutException'ı
        # yükseltmeye gerek yok, zaten bu bekleme de TimeoutException fırlatacak.
        self.wait_for_visible(self.ENTER_MANUALLY_BTN)
        print("✅ Enter Manually butonu geri sonrası görünür")

    def is_home_visible(self, timeout=3):
        """
        Kısa bir timeout ile homepage'de olduğumuzu (Enter Manually görünürlüğü üzerinden) kontrol eder.
        Test akışlarında, yanlışlıkla fazladan back basmamak için kullanıyoruz.
        """
        return self.is_element_visible(self.ENTER_MANUALLY_BTN, timeout=timeout)

    def open_premium_page_from_home(self):
        """Homepage'de premium page butonuna tıkla (RectView)."""
        self.wait_and_click(self.PREMIUM_PAGE_BTN)

    def go_to_scan_qr_code(self):
        """Homepage'de Scan Qr Code butonuna tıkla."""
        self.wait_for_visible(self.SCAN_QR_CODE_BTN)
        self.wait_and_click(self.SCAN_QR_CODE_BTN)
