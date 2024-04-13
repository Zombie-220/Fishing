from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import sys, os
import time
import threading

from modules.SimpleComponents import Button
from modules.GlobalVariables import *
from modules.SettingsWindow import SettingsWindow
from modules.LogsWindow import LogsWindow

class MainWindow(QMainWindow):
    title: str = "title"
    isFishing: bool = False
    tryCatchFish: bool = False
    startThisTry: float = 0
    timeForTry: float = 22.0

    def __init__(self, title: str) -> None:
        QMainWindow.__init__(self)

        self.title: str = title
        self.icon = APP_ICON
        
        self.setObjectName("MainWindow")

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(self.icon))
        self.setFixedSize(300, 30)
        self.move((screenSize.width() // 2) - (self.width() // 2), 0)
        self.setStyleSheet(CSS)

        fishingThread = threading.Thread(target = self.fishing)
        fishingThread.start()

        self.settingsWindow = SettingsWindow(self)
        self.logsWindow = LogsWindow(self)

        self.btn_start = Button(self, "START", 2, 2, 75, 26, "btn_standart", self.startFishing)
        btn_close = Button(self, EXIT_ICON, self.width() - 28, 2, 26, 26, "btn_red", self.windowShouldClose)
        btn_settings = Button(self, SETTING_ICON, self.width() - 56, 2, 26, 26, "btn_standart", self.openSettings)
        btn_logs = Button(self, LOGS_ICON, self.width() - 84, 2, 26, 26, "btn_standart", self.openLogsWindow)

    def openSettings(self):
        if self.settingsWindow.isVisible():
            self.settingsWindow.hide()
        else:
            self.settingsWindow.show()

    def openLogsWindow(self):
        if self.logsWindow.isVisible():
            self.logsWindow.hide()
        else:
            self.logsWindow.show()

    def startFishing(self):
        self.isFishing = not (self.isFishing)
        if self.isFishing:
            self.btn_start.setObjectName("btn_stop")
            self.btn_start.setText("STOP")
            self.isFishing = True
            self.logsWindow.logs.append([time.localtime(), "start"])
        else:
            self.btn_start.setObjectName("btn_standart")
            self.btn_start.setText("START")
            self.isFishing = False
            self.tryCatchFish = False
            self.logsWindow.logs.append([time.localtime(), "stop"])
        self.btn_start.setStyleSheet(CSS)

    def windowShouldClose(self):
        self.settingsWindow.close()
        self.logsWindow.close()
        self.close()

    def fishing(self):
        time.sleep(2)
        while self.isVisible():
            print("fishing")
            time.sleep(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    screenSize = app.primaryScreen().geometry()
    window = MainWindow("Auto fishing")
    window.show()
    sys.exit(app.exec())