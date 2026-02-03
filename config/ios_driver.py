from appium import webdriver
from appium.options.ios import XCUITestOptions
import os
from dotenv import load_dotenv

# .env dosyasını proje kök dizininden yükle
load_dotenv()


def get_ios_driver(test_name: str = "iOS Launch Test"):

    bs_user = os.getenv("BROWSERSTACK_USERNAME")
    bs_key = os.getenv("BROWSERSTACK_ACCESS_KEY")
    bs_app_ios = os.getenv("BS_APP_IOS")

    options = XCUITestOptions()
    options.platform_name = "iOS"
    options.automation_name = "XCUITest"
    options.device_name = "iPhone 14"
    # BrowserStack hata mesajına göre iPhone 14 için desteklenen
    # iOS sürümleri: 16, 18, 26. Burada 18'i kullanıyoruz.
    options.platform_version = "18"
    options.app = bs_app_ios  # bs://...
    options.no_reset = False
    options.auto_accept_alerts = True

    # BrowserStack meta bilgileri
    options.set_capability("project", "Authenticator Complete Flow")
    options.set_capability("build", "iOS Complete Flow")
    options.set_capability("name", test_name)

    driver = webdriver.Remote(
        command_executor=f"https://{bs_user}:{bs_key}@hub-cloud.browserstack.com/wd/hub",
        options=options,
    )

    return driver
