from pages.android.premium_page import PremiumPage
from pages.android.legal_page import LegalPage


def test_premium_legal_links(app):
    premium = PremiumPage(app)
    legal = LegalPage(app)

    premium.click_premium_banner()
    premium.skip_if_visible()

    premium.click_terms_of_service()
    legal.verify_terms_and_conditions_visible()
    premium.click_back_icon()

    premium.click_privacy_policy()
    legal.verify_privacy_policy_visible()
    premium.click_back_icon()

    premium.click_eula()
    legal.verify_eula_visible()
    premium.click_back_icon()
