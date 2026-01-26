from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class HomePage(BasePage):
    ENTER_MANUALLY_BTN = (AppiumBy.ACCESSIBILITY_ID, "Enter Manually")
    SCAN_QR_CODE_BTN = (AppiumBy.ACCESSIBILITY_ID, "Scan Qr Code")
    PREMIUM_PAGE_BTN = (By.XPATH, "//com.horcrux.svg.RectView")
    TOP_RIGHT_BUTTON = (
        By.XPATH,
        "//android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup[2]/com.horcrux.svg.SvgView/com.horcrux.svg.GroupView/com.horcrux.svg.PathView",
    )

    def go_to_add_key(self):
        self.wait_for_visible(self.ENTER_MANUALLY_BTN)
        self.wait_and_click(self.ENTER_MANUALLY_BTN)

    def click_top_right_button(self):
        """Sağ üstteki butona tıkla"""
        self.wait_and_click(self.TOP_RIGHT_BUTTON)

    def verify_enter_manually_visible(self):
        """Enter Manually butonunun görünür olduğunu doğrula"""
        self.wait_for_visible(self.ENTER_MANUALLY_BTN)
        print("✅ Enter Manually butonu görünür")

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
