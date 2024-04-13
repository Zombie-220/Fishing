from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import sys
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
    thisTryCatch: bool = False
    startThisTry: int = 0
    startTime: int = -1
    logs: list = []

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
        btn_close = Button(self, EXIT_ICON, self.width() - 30, 2, 26, 26, "btn_red", self.windowShouldClose)
        btn_settings = Button(self, SETTING_ICON, self.width() - 60, 2, 26, 26, "btn_standart", self.openSettings)
        btn_logs = Button(self, LOGS_ICON, self.width() - 90, 2, 26, 26, "btn_standart", self.openLogsWindow)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.checkLogs)
        self.timer.setInterval(500)
        self.timer.start()

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
            self.startTime = time.time()
            self.logs.append([time.localtime(), "start"])
        else:
            self.btn_start.setObjectName("btn_standart")
            self.btn_start.setText("START")
            self.isFishing = False
            self.tryCatchFish = False
            self.startTime = -1
            self.thisTryCatch = False
            self.logs.append([time.localtime(), "stop"])
        self.btn_start.setStyleSheet(CSS)

    def windowShouldClose(self):
        self.settingsWindow.close()
        self.logsWindow.close()
        self.close()

    def checkLogs(self):
        if len(self.logs) != 0:
            try:
                for i in range(len(self.logs)):
                    self.logsWindow.addLog(self.logs[i][0], self.logs[i][1])
                    self.logs.pop(i)
            except: pass
        self.timer.start()

    def fishing(self):
        time.sleep(2)
        # your fishing script

if __name__ == "__main__":
    app = QApplication(sys.argv)
    screenSize = app.primaryScreen().geometry()
    window = MainWindow("Auto fishing")
    window.show()
    sys.exit(app.exec())

    # Release
#  pyinstaller -w -F -i"images\icons\APP_ICON.ico" main.py

    # Debuging
#  pyinstaller -F -i"images\icons\APP_ICON.ico" main.py