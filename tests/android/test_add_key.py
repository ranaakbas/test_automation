from pages.android.home_page import HomePage
from pages.android.add_key_page import AddKeyPage
from pages.android.premium_page import PremiumPage


def test_add_key_success(app):
    home = HomePage(app)
    add_key = AddKeyPage(app)
    premium = PremiumPage(app)

    home.go_to_add_key()
    add_key.fill_key_form(
        website="example.com", account="rana@example.com", key="ABCDEF123"
    )
    add_key.submit()

    premium.verify_premium_upsell_visible()
    premium.skip_if_visible()
    add_key.click_back()

    home.verify_enter_manually_visible()
