import time
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException


class BasePage:
    def __init__(self, driver, timeout=30, human_mode=True):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.human_mode = human_mode

    # ---------------- HUMAN WAIT ----------------
    def _pause(self, min_s=0.3, max_s=0.9):
        if self.human_mode:
            time.sleep(random.uniform(min_s, max_s))

    # ---------------- CORE ACTIONS ----------------
    def wait_for_presence(self, locator):
        el = self.wait.until(EC.presence_of_element_located(locator))
        self._pause()
        return el

    def wait_for_visible(self, locator):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        self._pause()
        return el

    def is_element_visible(self, locator, timeout=3):
        """
        Verilen locator'ın kısa bir süre içinde görünür olup olmadığını bool olarak döner.
        Exception fırlatmak yerine True/False vermesi, akış kararları için kullanışlıdır.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            self._pause()
            return True
        except TimeoutException:
            return False

    def wait_and_click(self, locator):
        self._pause(0.2, 0.5)
        self.wait.until(EC.element_to_be_clickable(locator)).click()
        self._pause(0.4, 0.8)

    def hide_keyboard_if_open(self):
        try:
            self.driver.hide_keyboard()
            print("⌨️ Keyboard kapatıldı")
        except WebDriverException:
            print("ℹ️ Keyboard zaten kapalı / kapatılamadı")

    def press_back_button(self):
        """Telefonun geri tuşuna bas"""
        self.driver.back()
        self._pause(0.5, 1.0)
        print("🔙 Telefon geri tuşuna basıldı")

    # ---------------- INPUT ----------------
    def send_keys_human(self, locator, text):
        el = self.wait_for_visible(locator)

        self._pause(0.3, 0.6)
        el.click()
        self._pause(0.2, 0.4)

        el.send_keys(text)

        self._pause(0.4, 0.8)

    # ---------------- SCROLL ----------------
    def swipe_up_from_middle(self):
        self._pause(0.4, 0.7)

        size = self.driver.get_window_size()
        start_x = size["width"] // 2
        start_y = int(size["height"] * 0.65)
        end_y = int(size["height"] * 0.15)

        # W3C Actions kullanarak swipe (BrowserStack ve lokal Appium için uyumlu)
        finger = PointerInput(interaction.POINTER_TOUCH, "finger")
        actions = ActionBuilder(self.driver, mouse=finger)

        actions.pointer_action.move_to_location(start_x, start_y)
        actions.pointer_action.pointer_down()
        actions.pointer_action.pause(0.1)
        actions.pointer_action.move_to_location(start_x, end_y)
        actions.pointer_action.pause(0.1)
        actions.pointer_action.pointer_up()

        actions.perform()

        self._pause(0.6, 1.0)

    # ---------------- FIND WITH SWIPE ----------------
    def find_element_with_swipe(self, locator, max_swipe=5):
        for _ in range(max_swipe):
            try:
                el = self.driver.find_element(*locator)
                self._pause(0.3, 0.5)
                return el
            except NoSuchElementException:
                self.swipe_up_from_middle()

        raise Exception("❌ Element bulunamadı (swipe sonrası)")

    def _is_element_in_viewport(self, element):
        """
        Elementin gerçekten ekranda görünür alanda olup olmadığını kontrol eder.
        """
        try:
            location = element.location
            size = element.size
            window_size = self.driver.get_window_size()

            el_top = location["y"]
            el_bottom = location["y"] + size["height"]
            el_left = location["x"]
            el_right = location["x"] + size["width"]

            # Element ekran sınırları içinde mi?
            # Üstten ve alttan biraz margin bırak (header/footer için)
            margin_top = 100
            margin_bottom = 150

            in_viewport = (
                el_top >= margin_top
                and el_bottom <= (window_size["height"] - margin_bottom)
                and el_left >= 0
                and el_right <= window_size["width"]
            )

            print(
                f"📍 Element pozisyon: y={el_top}-{el_bottom}, "
                f"ekran: 0-{window_size['height']}, viewport'ta: {in_viewport}"
            )
            return in_viewport
        except Exception as e:
            print(f"⚠️ Viewport kontrolü başarısız: {e}")
            return False

    def swipe_until_visible_and_click(self, locator, max_swipe=10, min_swipe=0):
        element_found = False
        found_at_swipe = 0

        for i in range(1, max_swipe + 1):
            print(f"🔍 Element aranıyor (deneme {i})")

            try:
                el = self.driver.find_element(*locator)
            except NoSuchElementException:
                print(f"🔄 Element DOM'da yok, swipe #{i}")
                self.swipe_up_from_middle()
                continue

            # Element DOM'da var, ama ekranda görünür alanda mı?
            if not self._is_element_in_viewport(el):
                print(f"🔄 Element ekran dışında, swipe #{i}")
                self.swipe_up_from_middle()
                continue

            # Element görünür alanda bulundu
            element_found = True
            found_at_swipe = i

            # En az min_swipe kadar swipe yapılmadıysa devam et
            if i < min_swipe:
                print(
                    f"🔄 Element bulundu ama en az {min_swipe} swipe yapılmalı (şu an: {i}), swipe devam ediyor"
                )
                self.swipe_up_from_middle()
                continue

            # Element görünür alanda ve min_swipe tamamlandı, tıklamayı dene
            self._pause(0.3, 0.5)
            try:
                el = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable(locator)
                )
                print(f"✅ Element tıklanabilir durumda")
                el.click()
                self._pause(0.5, 0.8)
                print(f"✅ Element tıklandı")
                return True
            except TimeoutException:
                print(f"⚠️ Element tıklanamadı, swipe devam ediyor")
                self.swipe_up_from_middle()

        if element_found:
            print(f"❌ Element bulundu (swipe #{found_at_swipe}) ama tıklanamadı")
        else:
            print("❌ Element bulunamadı")
        return False
