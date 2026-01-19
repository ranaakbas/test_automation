from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "emulator-5554"
options.automation_name = "UiAutomator2"
options.app = "/Users/ranaakbas/mobiva/apks/app-release.apk"
options.no_reset = False
options.full_reset = False

driver = webdriver.Remote(command_executor="http://127.0.0.1:4723", options=options)

wait = WebDriverWait(driver, 30)


def swipe_up_from_middle(driver):
    size = driver.get_window_size()

    start_x = size["width"] // 2
    start_y = int(size["height"] * 0.65)
    end_y = int(size["height"] * 0.25)

    driver.execute_script(
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


def find_skip_button(driver, max_swipe=5):
    for i in range(max_swipe):
        try:
            return driver.find_element(By.XPATH, "//*[contains(@text,'Skip for now')]")
        except NoSuchElementException:
            swipe_up_from_middle(driver)
            time.sleep(1)

    raise Exception("❌ Skip for now bulunamadı")


# -------------------------------------------------
# ONBOARD 1
wait.until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Maximum Privacy')]"))
)

wait.until(
    EC.element_to_be_clickable((By.XPATH, "//*[contains(@text,'Continue')]"))
).click()

# -------------------------------------------------
# ONBOARD 2
wait.until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(@text,'Easy Setup')]"))
)

wait.until(
    EC.element_to_be_clickable((By.XPATH, "//*[contains(@text,'Continue')]"))
).click()

# -------------------------------------------------
# ONBOARD 3
wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//*[contains(@text,'Secure All Your Accounts')]")
    )
)

wait.until(
    EC.element_to_be_clickable((By.XPATH, "//*[contains(@text,'Get Started')]"))
).click()

# -------------------------------------------------
# PREMIUM PAYWALL
wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//*[contains(@text,'Maximum Security')]")
    )
)

skip_button = find_skip_button(driver)
skip_button.click()

# -------------------------------------------------
# HOMEPAGE
wait.until(
    EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Enter Manually"))
).click()

# -------------------------------------------------
# INPUTLAR
website_input = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//android.widget.EditText[@text='Enter website name']")
    )
)
website_input.send_keys("example.com")

account_input = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//android.widget.EditText[@text='user@example.com']")
    )
)
account_input.send_keys("rana@example.com")

key_input = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//android.widget.EditText[@text='_ _ _  _ _ _  _ _ _']")
    )
)
key_input.send_keys("ABCDEF123")

# -------------------------------------------------
# ADD KEY
# -------------------------------------------------
wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Add Key"))).click()

# -------------------------------------------------
# PREMIUM PAYWALL AGAIN
wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//*[contains(@text,'Maximum Security')]")
    )
)

print("✅SUCCESS.")

driver.quit()
