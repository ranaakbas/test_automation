import time

from selenium.common.exceptions import TimeoutException
from pages.android.premium_page import PremiumPage
from pages.android.legal_page import LegalPage
from pages.android.home_page import HomePage


def test_premium_legal_links(app):
    premium = PremiumPage(app)
    legal = LegalPage(app)
    home = HomePage(app)

    home.click_top_right_button()

    premium.click_premium_banner()
    premium.skip_if_visible()

    premium.click_terms_of_service()
    legal.verify_terms_and_conditions_visible()
    legal.check_scrollable()
    premium.click_back_icon()

    premium.click_privacy_policy()
    legal.verify_privacy_policy_visible()
    legal.check_scrollable()
    premium.click_back_icon()

    premium.click_eula()
    legal.verify_eula_visible()
    legal.check_scrollable()
    premium.click_back_icon()

    premium.click_contact_us()
    time.sleep(3)  # 3 saniye bekle

    legal.press_back_button()

    try:
        premium.wait_until_premium_actions_visible(timeout_s=5)

        premium.click_back_button()
    except TimeoutException:
        if home.is_home_visible(timeout=5):
            print("ℹ️ Doğrudan homepage'e dönülmüş, ekstra back yapılmayacak")
        else:
            print(
                "⚠️ Ne premium ne homepage görünüyor, son çare: telefon geri tuşu (1x)"
            )
            legal.press_back_button()
            print("✅ Telefon geri tuşu ile geri dönüldü (fallback)")

    home.verify_enter_manually_visible()

    home.open_premium_page_from_home()

    premium.skip_if_visible()
