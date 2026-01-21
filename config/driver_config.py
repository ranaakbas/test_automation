import os
from pathlib import Path
from appium import webdriver
from appium.options.android import UiAutomator2Options
from dotenv import load_dotenv

# .env dosyasını proje kök dizininden yükle
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


def get_driver(local=None, test_name="Test"):
    if local is None:
        local = os.getenv("USE_LOCAL", "false").lower() == "true"

    options = UiAutomator2Options()

    if local:
        options.device_name = "emulator-5554"
        options.automation_name = "UiAutomator2"
        options.app = os.getenv("LOCAL_APP_PATH")
        options.no_reset = False
        options.full_reset = False
        return webdriver.Remote("http://127.0.0.1:4723", options=options)

    # BrowserStack
    options.set_capability("app", os.getenv("BS_APP_URL"))
    options.set_capability("deviceName", "Samsung Galaxy S22")
    options.set_capability("os_version", "12.0")

    options.set_capability("project", "AddKey Automation")
    options.set_capability("build", "Android AddKey v1")
    options.set_capability("name", test_name)

    options.set_capability("automationName", "UiAutomator2")

    bs_user = os.getenv("BROWSERSTACK_USERNAME")
    bs_key = os.getenv("BROWSERSTACK_ACCESS_KEY")

    return webdriver.Remote(
        f"https://{bs_user}:{bs_key}@hub.browserstack.com/wd/hub", options=options
    )
