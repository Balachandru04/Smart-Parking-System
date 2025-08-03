import sys
import os
from InstallWindow import InstallWindow
from LoginWindow import LoginScreen
from PyQt5.QtWidgets import QApplication, QSplashScreen, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer

app = QApplication(sys.argv)

# Global window references
mainScreen = None
installWindow = None
loginWindow = None

class MainScreen:
    def __init__(self):
        self.loadSplashScreen()

    def loadSplashScreen(self):
        try:
            image_path = r"D:\Self_Learning\project\Data Analysics Projects\parking management system\python_vehicle.jpg"
            self.pix = QPixmap(image_path)
            if self.pix.isNull():
                raise FileNotFoundError(f"Splash image not found at: {image_path}")
            self.splash = QSplashScreen(self.pix, Qt.WindowStaysOnTopHint)
            self.splash.show()
        except Exception as e:
            self.showErrorMessage(f"Error loading splash screen:\n{e}")
            sys.exit(1)

    def closeSplash(self):
        self.splash.close()

    def showErrorMessage(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(message)
        msg_box.setWindowTitle("Error")
        msg_box.exec_()

def showSetupWindow():
    mainScreen.closeSplash()
    installWindow.show()

def showLoginWindow():
    mainScreen.closeSplash()
    loginWindow.showLoginScreen()

if __name__ == "__main__":
    # Instantiate windows here
    mainScreen = MainScreen()
    installWindow = InstallWindow()
    loginWindow = LoginScreen()

    # Show splash, then route
    if os.path.exists("./config.json"):
        QTimer.singleShot(3000, showLoginWindow)
    else:
        QTimer.singleShot(3000, showSetupWindow)

    sys.exit(app.exec_())
