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

# Vetex, this message is for you. If I get caught, I think I deserve to be praised...

# Ha-ha
# while I was writing the program I spent 10 days and caught only two sunken treasures (i caught 5000+ fish)
# but i got Expert Angler title, hah

def locate_image(img, threshold: float):
    screenshot = pyautogui.screenshot()
    screenshot = numpy.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

    result = cv2.matchTemplate(screenshot, img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        return (max_loc[0], max_loc[1])
    return None

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

    def __init__(self, title: str):
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
        btn_close = Button(self, EXIT_ICON, self.width() - 28, 2, 26, 26, "btn_red", self.closeEvent)
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

    def openSettings(self) -> None:
        if self.settingsWindow.isVisible():
            self.settingsWindow.hide()
        else:
            self.settingsWindow.show()

    def openLogsWindow(self) -> None:
        if self.logsWindow.isVisible():
            self.logsWindow.hide()
        else:
            self.logsWindow.show()

    def startFishing(self) -> None:
        self.isFishing = not (self.isFishing)
        if self.isFishing and not self.shouldStopFishing:
            self.btn_start.setObjectName("btn_red")
            self.btn_start.setText("STOP")
            self.btn_start.setToolTip("Stop fishing")
            self.isFishing = True
            self.startFishingTimer = time.time()
            self.startCheckTimer = time.time()
            self.logsWindow.logs.append([time.localtime(), "start"])
            self.setStyleSheet(CSS)
        else:
            self.shouldStopFishing = True

    def checkShouldStopFishing(self) -> None:
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

    def closeEvent(self, event) -> None:
        self.settingsWindow.close()
        self.logsWindow.close()
        self.close()

    def fishing(self) -> None:
        while self.isVisible():
            if self.isFishing:
                self.timeForWait = time.time() - self.startFishingTimer
                self.checkTimer = time.time() - self.startCheckTimer
                if (self.tryCatchFish or locate_image(IMG_START, 0.7)):
                    if not self.tryCatchFish:
                        self.tryCatchFish = True
                        pyautogui.click(button = "left")
                        self.startThisTry = time.time()

                    timeForThisTry = time.time() - self.startThisTry
                    if (locate_image(IMG_FISH, 0.7) or locate_image(IMG_JUNK, 0.7)) and (timeForThisTry <= self.timeForTry):
                        self.endTry("fish")
                        self.addFishCount()
                    else: pyautogui.click(button = "left")
                    if locate_image(IMG_TREASURE, 0.7) and (timeForThisTry <= self.timeForTry) and self.tryCatchFish:
                        self.endTry("treasure")
                        self.addFishCount()
                    else: pyautogui.click(button = "left")
                    if locate_image(IMG_SUNKEN, 0.7) and (timeForThisTry <= self.timeForTry) and self.tryCatchFish:
                        self.endTry("sunken")
                        self.addFishCount()
                    else: pyautogui.click(button = "left")
                    if timeForThisTry > self.timeForTry: self.endTry("timeError")
                    else: pyautogui.click(button = "left")
                
                elif self.timeForWait >= self.maxTimeForWait:
                    if (locate_image(CONNECT_ERR_1, 0.7)) or (locate_image(CONNECT_ERR_2, 0.7)) or (locate_image(CONNECT_ERR_3, 0.7)): self.shouldStopFishing = True
                    else: self.endTry("timeError")

                elif (self.checkTimer >= self.settingsWindow.checkTime) and (self.settingsWindow.usePotion or self.settingsWindow.useMeal):
                    if self.settingsWindow.usePotion:
                        keyboard.press_and_release(f"{self.settingsWindow.potionKey}")
                        if self.settingsWindow.potionKey != 'e':
                            pyautogui.click(button = "left")
                            time.sleep(0.75)
                            keyboard.press_and_release(f"{self.settingsWindow.rodKey}")
                            pyautogui.click(button = "left")
                    if self.settingsWindow.useMeal:
                        keyboard.press_and_release(f"{self.settingsWindow.mealKey}")
                        pyautogui.click(button = "left")
                        time.sleep(0.75)
                        keyboard.press_and_release(f"{self.settingsWindow.rodKey}")
                        pyautogui.click(button = "left") 
                    self.logsWindow.logs.append([time.localtime(), "consume"])
                    self.startFishingTimer = time.time()
                    self.startCheckTimer = time.time()

                time.sleep(0.25)

    def endTry(self, log: str) -> None:
        rodKey = f"{self.settingsWindow.rodKey}"
        self.tryCatchFish = False
        self.startFishingTimer = time.time()
        self.logsWindow.logs.append([time.localtime(), log])
        time.sleep(0.2)
        keyboard.press_and_release(rodKey)
        keyboard.press_and_release(rodKey)
        time.sleep(0.2)
        pyautogui.click(button = "left")

    def addFishCount(self) -> None:
        self.fishCount += 1
        self.__countLabel.setText(f"Caught: {self.fishCount}")

    def resetFishCount(self) -> None:
        self.fishCount = 0
        self.__countLabel.setText(f"Caught: {self.fishCount}")

if __name__ == "__main__":
    IMG_START = cv2.imread(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}/images/forScript/start.png')
    IMG_FISH = cv2.imread(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}/images/forScript/fish.png')
    IMG_TREASURE = cv2.imread(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}/images/forScript/treasure.png')
    IMG_JUNK = cv2.imread(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}/images/forScript/junk.png')
    IMG_SUNKEN = cv2.imread(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}/images/forScript/sunken.png')
    CONNECT_ERR_1 = cv2.imread(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}/images/forScript/internetError_1.png')
    CONNECT_ERR_2 = cv2.imread(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}/images/forScript/internetError_2.png')
    CONNECT_ERR_3 = cv2.imread(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}/images/forScript/internetError_3.png')

    app = QApplication(sys.argv)
    screenSize = app.primaryScreen().geometry()
    window = MainWindow("Auto fishing")
    window.show()
    window.fishingThread.start()
    sys.exit(app.exec())

#  pyinstaller -w -F -i"images\icons\APP_ICON.ico" -n "auto fishing" main.py