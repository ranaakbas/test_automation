import pytest
from config import get_driver
from pages.android.onboard_page import OnboardPage
from pages.android.premium_page import PremiumPage


@pytest.fixture(scope="function")
def app():
    driver = get_driver(test_name="Android Tests")

    onboard = OnboardPage(driver)
    premium = PremiumPage(driver)

    onboard.complete_onboarding()
    premium.skip_if_visible()

    yield driver

    driver.quit()
