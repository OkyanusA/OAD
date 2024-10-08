from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import os
import subprocess

class OADApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.remaining_time = 180  # 180 saniye (3 dakika)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("OAD - Tam Ekran Modu")
        self.setGeometry(0, 0, QtWidgets.QDesktopWidget().screenGeometry().width(), QtWidgets.QDesktopWidget().screenGeometry().height())
        self.setWindowState(QtCore.Qt.WindowFullScreen)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: #FFFFFF;")  

        # Label
        self.label = QtWidgets.QLabel("OAD Aktif - Lütfen USB Anahtarını Takın\nNot: Süre dolunca sistem kapanacaktır.", self)
        self.label.setFont(QtGui.QFont("Arial", 24, QtGui.QFont.Bold))
        self.label.setStyleSheet("color: #000000;")  
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setGeometry(self.width() // 4, self.height() // 2 - 50, self.width() // 2, 150)

        # Zamanlayıcıyı başlat (USB kontrolü için)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.check_for_usb_key)
        self.timer.start(3000)  # Her 3 saniyede bir kontrol et

        # Geri sayım göstergesi
        self.countdown_label = QtWidgets.QLabel(self)
        self.countdown_label.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Bold))
        self.countdown_label.setStyleSheet("color: #FF0000;")  # Kırmızı renkli geri sayım
        self.countdown_label.setAlignment(QtCore.Qt.AlignCenter)
        self.countdown_label.setGeometry(self.width() // 4, self.height() // 2 + 100, self.width() // 2, 50)
        self.update_countdown_label()

        # Geri sayım zamanlayıcısı
        self.countdown_timer = QtCore.QTimer(self)
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.countdown_timer.start(1000)  # Her saniye geri sayımı güncelle

    def update_countdown_label(self):
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.countdown_label.setText(f"Kalan Süre: {minutes:02d}:{seconds:02d}")

    def update_countdown(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.update_countdown_label()
        else:
            self.restart_system()  # Süre dolunca sistemi yeniden başlat

    def check_for_usb_key(self):
        # USB sürücülerini kontrol et
        drives = [f"{d}:\\" for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{d}:\\") and os.path.isdir(f"{d}:\\") and os.path.ismount(f"{d}:\\")]
        try:
            for drive in drives:
                key_file_path = os.path.join(drive, "anahtar.dat")
                if os.path.exists(key_file_path):
                    with open(key_file_path, 'r') as key_file:
                        content = key_file.read().strip()
                        if "OAD_ANAHTAR: " in content:
                            self.deactivate_app()
                            break
        except Exception as e:
            print(f"Hata: {e}")

    def deactivate_app(self):
        # USB anahtarı takılıyken uygulamayı kapat
        self.timer.stop()
        self.countdown_timer.stop()
        QtWidgets.QMessageBox.information(self, "OAD Devre Dışı", "USB Anahtarı algılandı. OAD devre dışı bırakılıyor.")
        QtCore.QCoreApplication.instance().quit()

    def closeEvent(self, event):
        # Uygulamanın kapatılmasını engelle
        event.ignore()

    def restart_system(self):
        # Sistemi yeniden başlat
        if sys.platform == "win32":
            subprocess.call(["shutdown", "/r", "/t", "0"])
        elif sys.platform == "linux":
            subprocess.call(["systemctl reboot"])
        elif sys.platform == "darwin":
            subprocess.call(["sudo shutdown -r now"])

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = OADApp()
    window.show()
    sys.exit(app.exec_())
