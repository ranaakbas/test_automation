from appium import webdriver
from appium.options.android import UiAutomator2Options

from pages.onboard_page import OnboardPage
from pages.premium_page import PremiumPage
from pages.home_page import HomePage
from pages.add_key_page import AddKeyPage

options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "emulator-5554"
options.automation_name = "UiAutomator2"
options.app = "/Users/ranaakbas/mobiva/apks/app-release.apk"
options.no_reset = False
options.full_reset = False

driver = webdriver.Remote(command_executor="http://127.0.0.1:4723", options=options)

try:
    onboard = OnboardPage(driver)
    premium = PremiumPage(driver)
    home = HomePage(driver)
    add_key = AddKeyPage(driver)

    onboard.complete_onboarding()
    premium.skip_if_visible()

    home.go_to_add_key()

    add_key.fill_key_form(
        website="example.com", account="rana@example.com", key="ABCDEF123"
    )

    add_key.submit()

    premium.skip_if_visible()

    print("✅ SUCCESS – Premium paywall tekrar çıktı.")

finally:
    driver.quit()
