from pages.android.home_page import HomePage
from pages.android.camera_page import CameraPage
from pages.android.add_key_page import AddKeyPage
from pages.android.premium_page import PremiumPage


def test_camera_qr_flow(app):
    home = HomePage(app)
    camera = CameraPage(app)
    add_key = AddKeyPage(app)
    premium = PremiumPage(app)

    home.go_to_scan_qr_code()
    camera.allow_camera_permission_if_prompted()
    camera.click_enter_manually()
    add_key.click_back()

    camera.open_photo_gallery()
    camera.allow_limited_gallery_access_if_prompted()
    camera.select_existing_photo()

    premium.skip_if_visible()
    camera.back_to_home()
