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

    def swipe_until_visible_and_click(self, locator, max_swipe=5):
        """
        Element görünene kadar aynı koordinatlarla swipe eder,
        görünür olduğu anda click eder.
        """
        for i in range(1, max_swipe + 1):
            try:
                print(f"🔍 Skip aranıyor (deneme {i})")
                el = WebDriverWait(self.driver, 2).until(
                    EC.visibility_of_element_located(locator)
                )
                print(f"✅ Element göründü (swipe #{i})")
                el.click()
                self._pause(0.4, 0.7)
                return True

            except TimeoutException:
                print(f"🔄 Swipe #{i}")
                self.swipe_up_from_middle()

        print("ℹ️ Skip for now bulunamadı")
        return False
