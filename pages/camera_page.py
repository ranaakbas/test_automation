from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class CameraPage(BasePage):
    """
    Scan QR Code (kamera) ekranı + izin popup'ları + Photo Gallery akışı.
    """

    # Kamera ekranındaki aksiyonlar
    ENTER_MANUALLY_BTN = (AppiumBy.ACCESSIBILITY_ID, "Enter Manually")
    PHOTO_GALLERY_BTN = (AppiumBy.ACCESSIBILITY_ID, "Photo Gallery")

    # Kamera ekranından geri (istek.md: content-desc: Scan Qr Code)
    BACK_TO_HOME_BTN = (AppiumBy.ACCESSIBILITY_ID, "Scan Qr Code")

    # Android permission dialog
    PERMISSION_DIALOG = (By.ID, "com.android.permissioncontroller:id/grant_dialog")
    ALLOW_WHILE_USING_APP = (
        By.ID,
        "com.android.permissioncontroller:id/permission_allow_foreground_only_button",
    )
    ALLOW_ALL_GALLERY_ACCESS = (
        By.ID,
        "com.android.permissioncontroller:id/permission_allow_all_button",
    )
    ALLOW_GALLERY_ACCESS = (
        By.ID,
        "com.android.permissioncontroller:id/permission_allow_button",
    )

    # Photo gallery modal (Compose) - opsiyonel, bazı cihazlarda olmayabilir
    GALLERY_MODAL = (
        By.XPATH,
        "//androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View",
    )

    # Farklı cihazlar için alternatif fotoğraf locator'ları
    FIRST_PHOTO = (
        By.XPATH,
        "//androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View[5]/android.view.View[2]/android.view.View[2]/android.view.View",
    )

    # Android sistem photo picker alternatifleri
    PHOTO_IMAGEVIEW = (
        By.XPATH,
        "//android.widget.ImageView[contains(@content-desc, 'Photo') or contains(@content-desc, 'Image')]",
    )
    PHOTO_RECYCLERVIEW_ITEM = (
        By.XPATH,
        "//androidx.recyclerview.widget.RecyclerView//android.view.ViewGroup[1]",
    )
    PHOTO_RECYCLERVIEW_FRAMELAYOUT = (
        By.XPATH,
        "//androidx.recyclerview.widget.RecyclerView//android.widget.FrameLayout[1]",
    )
    PHOTO_GRID_ITEM = (
        By.XPATH,
        "//android.widget.GridView//android.view.View[1] | //android.widget.GridView//android.widget.ImageView[1]",
    )
    PHOTO_COMPOSE_VIEW = (
        By.XPATH,
        "//androidx.compose.ui.platform.ComposeView//android.view.View[contains(@clickable, 'true')][1]",
    )
    # Android 13+ sistem photo picker için genel locator
    PHOTO_ANY_VIEWGROUP = (
        By.XPATH,
        "//androidx.recyclerview.widget.RecyclerView//android.view.ViewGroup[@clickable='true'][1]",
    )
    PHOTO_ANY_FRAMELAYOUT = (
        By.XPATH,
        "//androidx.recyclerview.widget.RecyclerView//android.widget.FrameLayout[@clickable='true'][1]",
    )

    # Sistem photo picker "Done" (cihaz/ROM'a göre değişebiliyor)
    DONE_TEXT_BTN = (By.XPATH, "//*[@text='Done' or @content-desc='Done']")
    DONE_DOCSUI_BTN = (By.ID, "com.android.documentsui:id/action_mode_done")
    DONE_PHOTOS_BTN = (By.ID, "com.google.android.apps.photos:id/done")

    def allow_camera_permission_if_prompted(self):
        """Kamera izni popup'ı gelirse 'While using app' seç."""
        try:
            WebDriverWait(self.driver, 4).until(
                EC.visibility_of_element_located(self.PERMISSION_DIALOG)
            )
        except TimeoutException:
            return False

        self.wait_and_click(self.ALLOW_WHILE_USING_APP)
        return True

    def click_enter_manually(self):
        """Kamera ekranında Enter Manually tıkla."""
        self.wait_and_click(self.ENTER_MANUALLY_BTN)

    def open_photo_gallery(self):
        """Kamera ekranında Photo Gallery tıkla."""
        self.wait_and_click(self.PHOTO_GALLERY_BTN)

    def allow_all_gallery_access_if_prompted(self):
        """
        Galeri izni popup'ı gelirse 'Allow all' veya 'Allow' seç.
        Bazı cihazlarda (örn. Galaxy S23) sadece 'Allow' butonu olabilir.
        """
        try:
            WebDriverWait(self.driver, 4).until(
                EC.visibility_of_element_located(self.PERMISSION_DIALOG)
            )
        except TimeoutException:
            return False

        # Önce 'Allow all' butonunu dene
        try:
            WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable(self.ALLOW_ALL_GALLERY_ACCESS)
            )
            self.wait_and_click(self.ALLOW_ALL_GALLERY_ACCESS)
            print("✅ 'Allow all' butonuna tıklandı")
            return True
        except TimeoutException:
            # 'Allow all' yoksa, basit 'Allow' butonunu dene
            try:
                WebDriverWait(self.driver, 2).until(
                    EC.element_to_be_clickable(self.ALLOW_GALLERY_ACCESS)
                )
                self.wait_and_click(self.ALLOW_GALLERY_ACCESS)
                print("✅ 'Allow' butonuna tıklandı (Allow all yoktu)")
                return True
            except TimeoutException:
                print("⚠️ İzin pop-up'ında Allow butonu bulunamadı")
                return False

    def allow_limited_gallery_access_if_prompted(self):
        """Artık sadece 'Allow all' kullanılıyor (limited yok)."""
        return self.allow_all_gallery_access_if_prompted()

    def select_existing_photo(self):
        """
        Photo gallery modal açıldıktan sonra varolan bir fotoğraf seç ve gerekiyorsa Done ile onayla.
        Farklı cihazlarda farklı yapılar olabileceği için birden fazla locator denenir.
        """
        # Photo picker'ın açılması için kısa bir bekleme
        self._pause(1.0, 1.5)

        # GALLERY_MODAL opsiyonel - bazı cihazlarda olmayabilir
        try:
            WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(self.GALLERY_MODAL)
            )
            print("✅ Gallery modal görünür")
        except TimeoutException:
            print("ℹ️ Gallery modal bulunamadı, alternatif locator'lar deneniyor...")

        # Fotoğraf seçimi için birden fazla alternatif dene
        photo_selected = False

        # 1. İlk deneme: Orijinal FIRST_PHOTO locator'ı
        try:
            WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(self.FIRST_PHOTO)
            )
            self.wait_and_click(self.FIRST_PHOTO)
            print("✅ Fotoğraf seçildi (FIRST_PHOTO)")
            photo_selected = True
        except TimeoutException:
            pass

        # 2. Deneme: RecyclerView içindeki ilk ViewGroup item
        if not photo_selected:
            try:
                WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable(self.PHOTO_RECYCLERVIEW_ITEM)
                )
                self.wait_and_click(self.PHOTO_RECYCLERVIEW_ITEM)
                print("✅ Fotoğraf seçildi (RecyclerView ViewGroup)")
                photo_selected = True
            except TimeoutException:
                pass

        # 2b. Deneme: RecyclerView içindeki tıklanabilir ViewGroup
        if not photo_selected:
            try:
                WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable(self.PHOTO_ANY_VIEWGROUP)
                )
                self.wait_and_click(self.PHOTO_ANY_VIEWGROUP)
                print("✅ Fotoğraf seçildi (RecyclerView tıklanabilir ViewGroup)")
                photo_selected = True
            except TimeoutException:
                pass

        # 2c. Deneme: RecyclerView içindeki FrameLayout
        if not photo_selected:
            try:
                WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable(self.PHOTO_RECYCLERVIEW_FRAMELAYOUT)
                )
                self.wait_and_click(self.PHOTO_RECYCLERVIEW_FRAMELAYOUT)
                print("✅ Fotoğraf seçildi (RecyclerView FrameLayout)")
                photo_selected = True
            except TimeoutException:
                pass

        # 2d. Deneme: RecyclerView içindeki tıklanabilir FrameLayout
        if not photo_selected:
            try:
                WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable(self.PHOTO_ANY_FRAMELAYOUT)
                )
                self.wait_and_click(self.PHOTO_ANY_FRAMELAYOUT)
                print("✅ Fotoğraf seçildi (RecyclerView tıklanabilir FrameLayout)")
                photo_selected = True
            except TimeoutException:
                pass

        # 3. Deneme: GridView içindeki ilk item
        if not photo_selected:
            try:
                WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable(self.PHOTO_GRID_ITEM)
                )
                self.wait_and_click(self.PHOTO_GRID_ITEM)
                print("✅ Fotoğraf seçildi (GridView item)")
                photo_selected = True
            except TimeoutException:
                pass

        # 4. Deneme: ComposeView içindeki tıklanabilir view
        if not photo_selected:
            try:
                WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable(self.PHOTO_COMPOSE_VIEW)
                )
                self.wait_and_click(self.PHOTO_COMPOSE_VIEW)
                print("✅ Fotoğraf seçildi (ComposeView)")
                photo_selected = True
            except TimeoutException:
                pass

        # 5. Deneme: ImageView ile fotoğraf bulma
        if not photo_selected:
            try:
                # Tüm ImageView'ları bul ve ilk tıklanabilir olanı seç
                imageviews = self.driver.find_elements(*self.PHOTO_IMAGEVIEW)
                if imageviews:
                    for img in imageviews[:3]:  # İlk 3'ü dene
                        try:
                            if img.is_displayed() and img.is_enabled():
                                img.click()
                                print("✅ Fotoğraf seçildi (ImageView)")
                                photo_selected = True
                                self._pause(0.5, 0.8)
                                break
                        except Exception:
                            continue
            except Exception:
                pass

        # 6. Son deneme: Tüm tıklanabilir view'ları bul ve ilkini seç
        if not photo_selected:
            try:
                # Tüm tıklanabilir elementleri bul
                clickable_elements = self.driver.find_elements(
                    By.XPATH, "//*[@clickable='true' or @enabled='true']"
                )

                # Ekranın görünür alanındaki ilk tıklanabilir elementi seç
                size = self.driver.get_window_size()
                for elem in clickable_elements[:10]:  # İlk 10 elementi dene
                    try:
                        if elem.is_displayed():
                            location = elem.location
                            # Ekranın görünür alanında mı kontrol et
                            if (
                                0 < location["y"] < size["height"] * 0.9
                                and 0 < location["x"] < size["width"]
                            ):
                                elem.click()
                                print("✅ Tıklanabilir element bulundu ve seçildi")
                                photo_selected = True
                                self._pause(0.5, 0.8)
                                break
                    except Exception:
                        continue
            except Exception as e:
                print(f"⚠️ Tıklanabilir element araması başarısız: {e}")

        # 7. Son çare: Ekranın ortasına W3C Actions ile tap
        if not photo_selected:
            try:
                from selenium.webdriver.common.actions.action_builder import (
                    ActionBuilder,
                )
                from selenium.webdriver.common.actions.pointer_input import PointerInput
                from selenium.webdriver.common.actions import interaction

                size = self.driver.get_window_size()
                center_x = size["width"] // 2
                center_y = size["height"] // 2

                finger = PointerInput(interaction.POINTER_TOUCH, "finger")
                actions = ActionBuilder(self.driver, mouse=finger)
                actions.pointer_action.move_to_location(center_x, center_y)
                actions.pointer_action.pointer_down()
                actions.pointer_action.pause(0.1)
                actions.pointer_action.pointer_up()
                actions.perform()

                print("✅ Ekranın ortasına tıklandı (W3C Actions)")
                photo_selected = True
                self._pause(0.5, 0.8)
            except Exception as e:
                print(f"⚠️ Son çare tap başarısız: {e}")

        if not photo_selected:
            raise Exception(
                "❌ Hiçbir fotoğraf seçilemedi - photo picker yapısı tanınmıyor"
            )

        # Fotoğraf seçildikten sonra Done ile onayla (gerekirse)
        self._confirm_photo_selection_if_needed()

    def _confirm_photo_selection_if_needed(self):
        """
        Bazı cihazlarda foto seçimi sonrası 'Done' ile onaylamak gerekiyor.
        Mevcut sorunda Done'a önce basıp sonra seçiyor gibi bir sıralama olabiliyor;
        burada sıralamayı garanti ediyoruz: önce seçim, sonra Done (varsa).
        """
        for locator in (self.DONE_TEXT_BTN, self.DONE_DOCSUI_BTN, self.DONE_PHOTOS_BTN):
            try:
                WebDriverWait(self.driver, 2).until(
                    EC.element_to_be_clickable(locator)
                ).click()
                self._pause(0.4, 0.8)
                print("✅ Photo selection Done ile onaylandı")
                return True
            except TimeoutException:
                continue
        return False

    def back_to_home(self):
        """Kamera ekranından homepage'e geri dön."""
        try:
            self.wait_and_click(self.BACK_TO_HOME_BTN)
        except TimeoutException:
            self.press_back_button()
