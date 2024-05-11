from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon
import sys, os
import time
import threading
import cv2, pyautogui, numpy, keyboard

from modules.SimpleComponents import Button, Label
from modules.GlobalVariables import *
from modules.SettingsWindow import SettingsWindow
from modules.LogsWindow import LogsWindow

# Ha-ha
# while I was writing the program I spent 10 days and caught only two sunken treasures (i caught 5000+ fish)
# but i got Expert Angler title, hah

class MainWindow(QMainWindow):
    title: str = "title"
    isFishing: bool = False
    tryCatchFish: bool = False
    startThisTry: float = 0
    timeForTry: int = 30
    maxTimeForWait: int = 70
    startFishingTimer: float = 0
    startCheckTimer: float = 0
    checkTimer: int = 0
    shouldStopFishing: bool = False
    fishCount: int = 0

    def __init__(self, title: str) -> None:
        super().__init__()

        self.title: str = title
        self.icon = APP_ICON
        
        self.setObjectName("MainWindow")

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(self.icon))
        self.setFixedSize(300, 30)
        self.move((screenSize.width() // 2) - (self.width() // 2), 0)
        self.setStyleSheet(CSS)

        self.fishingThread = threading.Thread(target = self.fishing)

        self.settingsWindow = SettingsWindow(self)
        self.logsWindow = LogsWindow(self)

        self.btn_start = Button(self, "START", 2, 2, 75, 26, "btn_standart", self.startFishing)
        self.btn_start.setToolTip("Start fishing")
        btn_close = Button(self, EXIT_ICON, self.width() - 28, 2, 26, 26, "btn_red", self.windowShouldClose)
        btn_close.setToolTip("Close window")
        btn_settings = Button(self, SETTING_ICON, self.width() - 56, 2, 26, 26, "btn_standart", self.openSettings)
        btn_settings.setToolTip("Settings window")
        btn_logs = Button(self, LOGS_ICON, self.width() - 84, 2, 26, 26, "btn_standart", self.openLogsWindow)
        btn_logs.setToolTip("History window")
        self.__countLabel = Label(self, 79, 2, 135, 26, "", f"Caught: {self.fishCount}")

        self.ShouldStopFishingTimer = QTimer(self)
        self.ShouldStopFishingTimer.setInterval(500)
        self.ShouldStopFishingTimer.timeout.connect(self.checkShouldStopFishing)
        self.ShouldStopFishingTimer.start()

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
            self.btn_start.setObjectName("btn_red")
            self.btn_start.setText("STOP")
            self.btn_start.setToolTip("Stop fishing")
            self.isFishing = True
            self.startFishingTimer = time.time()
            self.startCheckTimer = time.time()
            self.logsWindow.logs.append([time.localtime(), "start"])
            self.resetFishCount()
            self.setStyleSheet(CSS)
        else:
            self.shouldStopFishing = True

    def checkShouldStopFishing(self):
        if self.shouldStopFishing:
            self.btn_start.setObjectName("btn_standart")
            self.btn_start.setText("START")
            self.btn_start.setToolTip("Start fishing")
            self.isFishing = False
            self.tryCatchFish = False
            self.logsWindow.logs.append([time.localtime(), "stop"])
            self.setStyleSheet(CSS)
            self.shouldStopFishing = False
        self.ShouldStopFishingTimer.start()

    def windowShouldClose(self):
        self.settingsWindow.close()
        self.logsWindow.close()
        self.close()

    def fishing(self):
        time.sleep(2)
        while self.isVisible():
            if self.isFishing:
                print("fishing")
                time.sleep(1)

    def addFishCount(self):
        self.fishCount += 1
        self.__countLabel.setText(f"Caught: {self.fishCount}")

    def resetFishCount(self):
        self.fishCount = 0
        self.__countLabel.setText(f"Caught: {self.fishCount}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    screenSize = app.primaryScreen().geometry()
    window = MainWindow("Auto fishing")
    window.show()
    window.fishingThread.start()
    sys.exit(app.exec())