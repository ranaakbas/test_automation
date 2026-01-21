import sys
from pathlib import Path

# Proje kök dizinini Python path'e ekle
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import get_driver
from pages.onboard_page import OnboardPage
from pages.premium_page import PremiumPage
from pages.home_page import HomePage
from pages.add_key_page import AddKeyPage

driver = get_driver(test_name="AddKey Flow Test")

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

    print("✅ SUCCESS")

finally:
    driver.quit()
