import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class BasePage:
    def __init__(self, driver, timeout=30):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_for_presence(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_and_click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def swipe_up_from_middle(self):
        size = self.driver.get_window_size()
        start_x = size["width"] // 2
        start_y = int(size["height"] * 0.65)
        end_y = int(size["height"] * 0.25)

        self.driver.execute_script(
            "mobile: swipeGesture",
            {
                "left": start_x,
                "top": end_y,
                "width": 1,
                "height": start_y - end_y,
                "direction": "up",
                "percent": 1.0,
            },
        )

    def find_element_with_swipe(self, locator, max_swipe=5):
        for _ in range(max_swipe):
            try:
                return self.driver.find_element(*locator)
            except NoSuchElementException:
                self.swipe_up_from_middle()
                time.sleep(1)
        raise Exception("❌ Element bulunamadı (swipe sonrası)")
