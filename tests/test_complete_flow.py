import sys
import time
from pathlib import Path

# Proje kök dizinini Python path'e ekle
sys.path.insert(0, str(Path(__file__).parent.parent))

from selenium.common.exceptions import TimeoutException

from config import get_driver
from pages.android.onboard_page import OnboardPage
from pages.android.premium_page import PremiumPage
from pages.android.home_page import HomePage
from pages.android.add_key_page import AddKeyPage
from pages.android.legal_page import LegalPage
from pages.android.camera_page import CameraPage


def test_complete_flow():
    """Uygulamanın tam akış senaryosunu çalıştırır.

    Herhangi bir adımda exception fırlarsa test FAIL olur.
    """
    driver = get_driver(test_name="Complete Flow Test")

    try:
        onboard = OnboardPage(driver)
        premium = PremiumPage(driver)
        home = HomePage(driver)
        add_key = AddKeyPage(driver)
        legal = LegalPage(driver)
        camera = CameraPage(driver)

        # Mevcut senaryo: app aç -> onboarding geç -> premium skip -> enter manually -> form doldur -> add key -> premium skip
        onboard.complete_onboarding()
        premium.skip_if_visible()

        home.go_to_add_key()

        add_key.fill_key_form(
            website="example.com", account="rana@example.com", key="ABCDEF123"
        )

        add_key.submit()

        premium.skip_if_visible()

        # Yeni senaryo: premium page kapandı, add key sayfasındayız
        print("\n📋 Yeni senaryo başlıyor...")

        # Add key sayfasından geri dön
        add_key.click_back()
        print("✅ Add Key sayfasından geri dönüldü")

        # Homepage'de sağ üstteki butona tıkla
        home.click_top_right_button()
        print("✅ Sağ üstteki butona tıklandı")

        # Premium banner'a tıkla
        premium.click_premium_banner()
        print("✅ Premium banner'a tıklandı")

        # Premium page'de en aşağıya kaydır ve skip for now'a tıkla
        premium.skip_if_visible()

        # Terms of Service butonuna tıkla
        premium.click_terms_of_service()
        legal.verify_terms_and_conditions_visible()
        legal.check_scrollable()
        premium.click_back_icon()
        print("✅ Terms of Service akışı tamamlandı")

        # Privacy Policy butonuna tıkla
        premium.click_privacy_policy()
        legal.verify_privacy_policy_visible()
        legal.check_scrollable()
        premium.click_back_icon()
        print("✅ Privacy Policy akışı tamamlandı")

        # EULA butonuna tıkla
        premium.click_eula()
        legal.verify_eula_visible()
        legal.check_scrollable()
        premium.click_back_icon()
        print("✅ EULA akışı tamamlandı")

        # Contact Us butonuna tıkla
        premium.click_contact_us()
        print("✅ Contact Us butonuna tıklandı, mail uygulaması açıldı")

        # Mail uygulamasını ekranda görmek için biraz bekle
        print("⏳ Mail uygulaması ekranda görüntüleniyor...")
        time.sleep(3)  # 3 saniye bekle

        # Mail uygulamasından geri dönmek için telefonun geri tuşuna bas
        # Not: Bazı cihazlarda önce Settings'e, bazı cihazlarda direkt uygulamaya dönülebiliyor.
        legal.press_back_button()
        print("✅ Mail uygulamasından geri dönmek için telefon geri tuşuna basıldı")

        # Burada iki ana durum var:
        # 1) Premium sayfasına (legal aksiyonların olduğu ekran) dönülmüş olabilir
        # 2) Ara ekranda (örn. Settings) back çalışıp doğrudan homepage'e dönülmüş olabilir
        try:
            premium.wait_until_premium_actions_visible(timeout_s=5)
            print("📱 Premium sayfası tekrar göründü")

            # Premium sayfasındaysak, uygulama içi Back ile kontrollü şekilde homepage'e dön
            premium.click_back_button()
            print("✅ Homepage'e premium üzerinden geri dönüldü")
        except TimeoutException:
            # Premium aksiyonları görünmüyorsa, homepage'de olup olmadığımızı kontrol et
            if home.is_home_visible(timeout=5):
                print("ℹ️ Doğrudan homepage'e dönülmüş, ekstra back yapılmayacak")
            else:
                # Ne premium ne de homepage görünür; testin tamamen kilitlenmesini
                # engellemek için son çare olarak bir kez daha telefon geri tuşu kullan.
                print(
                    "⚠️ Ne premium ne homepage görünüyor, son çare: telefon geri tuşu (1x)"
                )
                legal.press_back_button()
                print("✅ Telefon geri tuşu ile geri dönüldü (fallback)")

        # Homepage'de enter manually butonunun görünür olduğunu doğrula
        home.verify_enter_manually_visible()

        # ---------------- SENARYONUN DEVAMI ----------------
        print("\n📋 SENARYONUN DEVAMI başlıyor...")

        # Homepage de premium page butonunu bul - tıkla - premiumpage açılır
        home.open_premium_page_from_home()
        print("✅ Homepage premium page butonuna tıklandı")

        # Premium page açılır - swipe et - skipfornow tıkla
        premium.skip_if_visible()

        # Homepage tekrar görüneceğinden Scan QR code butonuna tıkla
        home.go_to_scan_qr_code()
        print("✅ Scan Qr Code butonuna tıklandı")

        # Kamera izni popup'ı gelirse "while using app" seç
        camera.allow_camera_permission_if_prompted()

        # Kamera ekranı görülür - enter manually tıkla - add key page gör
        camera.click_enter_manually()
        print("✅ Kamera ekranından Enter Manually tıklandı (Add Key açılmalı)")

        # Add key page'de işlem yok, sadece göründü mü kontrol ettik - back
        add_key.click_back()
        print("✅ Add Key'den geri dönüldü (kamera ekranına)")

        # Kamera ekranında photo gallery butonuna tıkla
        camera.open_photo_gallery()
        print("✅ Photo Gallery açıldı")

        # Galeri izni popup'ı gelirse allow limited access seç
        camera.allow_limited_gallery_access_if_prompted()

        # Photo gallery modal açılır - varolan fotoğrafı seçer
        camera.select_existing_photo()
        print("✅ Varolan fotoğraf seçildi")

        # Premium page açılır - swipe et - skipfornow tıkla
        premium.skip_if_visible()

        # Kamera sayfasına dönünce back butonuna bas (content-desc:Scan Qr Code) - homepage'e dön
        camera.back_to_home()

        # Anasayfaya dönünce testi bitir (enter manually butonu görünür)
        home.verify_enter_manually_visible()
        print("\n✅ SENARYONUN DEVAMI başarıyla tamamlandı!")

        print("\n✅ TÜM SENARYO BAŞARIYLA TAMAMLANDI!")
    finally:
        driver.quit()
