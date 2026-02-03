"""iOS için home sayfası - Android XPath yerine accessibility ID kullanır."""

from appium.webdriver.common.appiumby import AppiumBy

from pages.android.home_page import HomePage as AndroidHomePage


class HomePage(AndroidHomePage):
    """iOS HomePage - ENTER_MANUALLY, SCAN_QR_CODE zaten accessibility id ile çalışır.
    Premium ve top right buton için iOS locator'ları override edilir.
    """

    # iOS'ta premium/settings butonları - uygulama yapısına göre güncellenebilir
    PREMIUM_PAGE_BTN = (AppiumBy.ACCESSIBILITY_ID, "Maximum Security")
    TOP_RIGHT_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Premium")

    # iOS'ta sağ üstteki yıldızlı buton (premium) - info.md'deki xpath
    TOP_RIGHT_PREMIUM_BUTTON = (
        AppiumBy.XPATH,
        '//XCUIElementTypeApplication[@name="Authenticator"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[1]',
    )

    # iOS'ta sağ üstteki settings butonu - info.md'deki xpath
    TOP_RIGHT_SETTINGS_BUTTON = (
        AppiumBy.XPATH,
        '//XCUIElementTypeApplication[@name="Authenticator"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[2]',
    )

    def click_top_right_premium_button(self):
        """Sağ üstteki yıldızlı (premium) butona tıkla"""
        self.wait_and_click(self.TOP_RIGHT_PREMIUM_BUTTON)
        print("✅ Sağ üstteki premium butonuna tıklandı")

    def click_top_right_settings_button(self):
        """Sağ üstteki settings butonuna tıkla"""
        self.wait_and_click(self.TOP_RIGHT_SETTINGS_BUTTON)
        print("✅ Sağ üstteki settings butonuna tıklandı")
