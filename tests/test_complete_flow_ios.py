"""
iOS tam akış testi - BrowserStack üzerinde çalışır.

info.md senaryosuna göre:
- Allow tracking popup → Allow
- Onboard1 (Maximum Privacy) → Continue
- Onboard2 (Easy Setup) → Continue
- Onboard3 (Secure All Your Accounts) → Enjoying popup (Not now) → Get Started
- Premium paywall → scroll → Skip for now
- Homepage (Enter Manually) → test_complete_flow.py ile aynı işlemler
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from selenium.common.exceptions import TimeoutException

from config.ios_driver import get_ios_driver
from pages.ios.onboard_page import OnboardPage as IosOnboardPage
from pages.ios.premium_page import PremiumPage as IosPremiumPage
from pages.ios.home_page import HomePage as IosHomePage

# from pages.ios.add_key_page import AddKeyPage as IosAddKeyPage
from pages.ios.legal_page import LegalPage as IosLegalPage
from pages.ios.settings_page import SettingsPage as IosSettingsPage
from pages.android.camera_page import CameraPage


def test_complete_flow_ios():
    """iOS uygulamasının tam akış senaryosunu çalıştırır.

    BrowserStack + Appium + XCUITest ile iOS simülatöründe çalışır.
    """
    driver = get_ios_driver(test_name="iOS Complete Flow Test")

    try:
        onboard = IosOnboardPage(driver)
        premium = IosPremiumPage(driver)
        home = IosHomePage(driver)
        # add_key = IosAddKeyPage(driver)
        legal = IosLegalPage(driver)
        settings = IosSettingsPage(driver)
        camera = CameraPage(driver)

        # --- İlk kısım: Onboarding + Premium skip + Homepage ---
        onboard.complete_onboarding()
        premium.skip_if_visible()

        # home.go_to_add_key()

        # add_key.fill_key_form(
        #     website="example.com", account="rana@example.com", key="ABCDEF123"
        # )
        # add_key.submit()

        # premium.skip_if_visible()

        # # --- SENARYO DEVAMI (info.md'den) ---
        # print("\n📋 SENARYO DEVAMI başlıyor...")

        # # Add key page'den geri dön
        # add_key.click_back()
        # print("✅ Add Key sayfasından geri dönüldü")

        # Homepage görülecek, sağ üstteki settings butonuna tıkla
        home.click_top_right_settings_button()
        print("✅ Sağ üstteki settings butonuna tıklandı")

        # Settings ekranında premium banner'a tıkla
        settings.click_premium_banner()
        print("✅ Settings'te premium banner'a tıklandı")

        # Premium paywall skip for now ile çıkılacak
        premium.skip_if_visible()

        # Settings ekranına geri döndüğünde Terms of Service butonuna bas
        settings.click_terms_of_service()
        print("✅ Terms of Service butonuna tıklandı")

        # Kaydırılıyor mu diye bir kere kaydır
        legal.check_scrollable()

        # Üst solda back ikonundan settings ekranına geri dön
        settings.click_back_from_document()

        print("✅ Terms sayfasından settings'e geri dönüldü")

        # Settings ekranına geri döndüğünde Privacy Policy butonuna bas
        settings.click_privacy_policy()
        print("✅ Privacy Policy butonuna tıklandı")

        # Kaydırılıyor mu diye bir kere kaydır
        legal.check_scrollable()

        # Üst solda back ikonundan settings ekranına geri dön
        settings.click_back_from_document()
        print("✅ Privacy Policy sayfasından settings'e geri dönüldü")

        # Settings ekranına geri döndüğünde EULA butonuna bas
        settings.click_eula()
        print("✅ EULA butonuna tıklandı")

        # Kaydırılıyor mu diye bir kere kaydır
        legal.check_scrollable()

        # Üst solda back ikonundan settings ekranına geri dön
        settings.click_back_from_document()

        print("✅ EULA sayfasından settings'e geri dönüldü")

        # Settings ekranına geri döndüğünde back butonuna bas
        settings.click_back_to_home()
        print("✅ Settings'ten homepage'e geri dönüldü")

        # Homepage görülecek, sağ üstteki yıldızlı (premium) butona tıkla
        home.click_top_right_premium_button()
        print("✅ Sağ üstteki premium butonuna tıklandı")

        # Premium page çıkacak ve skip for now ile çıkılacak
        premium.skip_if_visible()

        # Homepage görülecek
        home.verify_enter_manually_visible()
        print("\n✅ SENARYO DEVAMI başarıyla tamamlandı!")

        print("\n✅ TÜM iOS SENARYO BAŞARIYLA TAMAMLANDI!")

    finally:
        driver.quit()
