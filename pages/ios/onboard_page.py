"""iOS için onboarding sayfası - Allow popup, onboard1/2/3,
Enjoying popup + alternatif Star popup handling."""

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class OnboardPage(BasePage):
    """iOS uygulaması için onboarding akışı - popup-safe."""

    # --- iOS system tracking popup ---
    ALLOW_TRACKING_BTN = (AppiumBy.ACCESSIBILITY_ID, "Allow")

    # --- Onboarding screens ---
    MAX_PRIVACY = (AppiumBy.ACCESSIBILITY_ID, "Maximum Privacy")
    EASY_SETUP = (AppiumBy.ACCESSIBILITY_ID, "Easy Setup")
    SECURE_ACCOUNTS = (AppiumBy.ACCESSIBILITY_ID, "Secure All Your Accounts")
    CONTINUE_BTN = (AppiumBy.ACCESSIBILITY_ID, "Continue")
    GET_STARTED_BTN = (AppiumBy.ACCESSIBILITY_ID, "Get Started")

    # --- Enjoying Authenticator popup ---
    # --- Enjoying Authenticator popup ---
    ENJOYING_POPUP = (AppiumBy.ACCESSIBILITY_ID, "Enjoying Authenticator?")
    NOT_NOW_BTN = (AppiumBy.ACCESSIBILITY_ID, "Not now")
    NOT_NOW_LABEL = (AppiumBy.IOS_PREDICATE, "label CONTAINS 'Not now'")

    # 🔥 XPath fallback (Inspector'dan alınan)
    NOT_NOW_XPATH = (
        AppiumBy.XPATH,
        "//XCUIElementTypeApplication[@name='Authenticator']"
        "/XCUIElementTypeWindow[1]"
        "/XCUIElementTypeOther[2]"
        "/XCUIElementTypeOther"
        "/XCUIElementTypeOther"
        "/XCUIElementTypeOther"
        "/XCUIElementTypeOther"
        "/XCUIElementTypeOther[2]"
        "/XCUIElementTypeOther[2]"
        "/XCUIElementTypeOther"
        "/XCUIElementTypeOther[2]"
        "/XCUIElementTypeOther[2]"
        "/XCUIElementTypeScrollView[2]"
        "/XCUIElementTypeOther[1]",
    )

    # --- Star popup (rate alternatif) ---
    STAR_POPUP_TITLE = (AppiumBy.IOS_PREDICATE, "label CONTAINS 'star pop-up'")
    STAR_POPUP_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "fdghjgk")
    STAR_POPUP_BUTTON_LABEL = (AppiumBy.IOS_PREDICATE, "label CONTAINS 'fdghjgk'")

    # ------------------------------------------------------------------ #

    def allow_tracking_if_prompted(self, timeout=5):
        """Tracking popup gelirse Allow'a bas."""
        try:
            el = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(self.ALLOW_TRACKING_BTN)
            )
            try:
                el.click()
            except StaleElementReferenceException:
                pass
            self._pause(0.5, 1.0)
            print("✅ Allow tracking popup kapatıldı")
            return True
        except TimeoutException:
            return False

    # ------------------------------------------------------------------ #

    def complete_onboarding(self):
        """
        Final iOS onboarding akışı (popup-safe):

        1. Allow tracking (varsa)
        2. Onboard 1 → Continue
        3. Onboard 2 → Continue
        4. Star / Enjoying popup (varsa)
        5. Onboard 3
        6. Star / Enjoying popup (tekrar çıkabilir)
        7. Get Started
        """
        self.allow_tracking_if_prompted()

        # Onboard 1
        self.wait_for_visible(self.MAX_PRIVACY)
        self._pause(0.5, 1.0)
        self.wait_and_click(self.CONTINUE_BTN)

        # Onboard 2
        self.wait_for_visible(self.EASY_SETUP)
        self._pause(0.5, 1.0)
        self.wait_and_click(self.CONTINUE_BTN)

        # Popup'lar burada çıkabiliyor
        self._dismiss_enjoying_popup_if_visible(timeout=5)

        # Onboard 3
        self.wait_for_visible(self.SECURE_ACCOUNTS)
        self._pause(0.5, 1.0)

        # Get Started
        self.wait_and_click(self.GET_STARTED_BTN)
        self._pause(0.5, 1.0)

    def wait_until_onboard3_ready(self, timeout=15):
        """
        Onboard3 ekranı gerçekten hazır olana kadar bekler.
        Önce popup'ları temizler, popup yokken Secure All'u doğrular.
        """
        end_time = time.time() + timeout

        while time.time() < end_time:

            popup_closed = False

            popup_closed |= self._dismiss_enjoying_popup_if_visible(timeout=1)

            if popup_closed:
                self._pause(0.5, 0.8)
                continue

            try:
                el = WebDriverWait(self.driver, 2).until(
                    EC.visibility_of_element_located(self.SECURE_ACCOUNTS)
                )
                print("✅ Onboard3 (Secure All) hazır")
                return el
            except TimeoutException:
                pass

        raise TimeoutException(
            "❌ Onboard3 ekranı timeout oldu (popup temizleme sonrası)"
        )

    # ------------------------------------------------------------------ #
    # POPUP HANDLERS
    # ------------------------------------------------------------------ #

    def _dismiss_enjoying_popup_if_visible(self, timeout=3):
        """Enjoying Authenticator popup'ı Not now ile kapat."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.ENJOYING_POPUP)
            )
            print("📱 Enjoying Authenticator popup tespit edildi")

            for locator in (self.NOT_NOW_XPATH, self.NOT_NOW_BTN, self.NOT_NOW_LABEL):
                try:
                    WebDriverWait(self.driver, 2).until(
                        EC.element_to_be_clickable(locator)
                    ).click()
                    self._pause(0.5, 1.0)
                    print("✅ Enjoying popup kapatıldı (Not now)")
                    return True
                except TimeoutException:
                    continue

            # iOS system alert fallback
            if self._try_dismiss_ios_alert():
                return True

        except TimeoutException:
            pass
        return False

    # ------------------------------------------------------------------ #

    def _try_dismiss_ios_alert(self):
        """iOS system alert dismiss."""
        try:
            self.driver.execute_script("mobile: alert", {"action": "dismiss"})
            self._pause(0.5, 1.0)
            print("✅ iOS alert dismiss edildi")
            return True
        except Exception:
            return False
