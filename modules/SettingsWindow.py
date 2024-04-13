from PyQt6 import QtWidgets, QtGui, QtCore

from modules.header import MainWindow
from modules.SimpleComponents import WindowTitleBar, Button, Entry, Label
from modules.GlobalVariables import CSS, EXIT_ICON

class SettingsWindow(QtWidgets.QMainWindow):
    isMeasuring: bool = False

    def __init__(self, parent: MainWindow):
        QtWidgets.QWidget.__init__(self)

        self.title = "Settings"
        self.icon = parent.icon

        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.icon))
        self.setFixedSize(250, 125)
        self.move(100, 100)
        self.setObjectName("Window")
        self.setStyleSheet(CSS)

        windowTitle = WindowTitleBar(self)
        btn_close = Button(self, EXIT_ICON, self.width() - 30, 2, 26, 26, "btn_red", self.closeWidow)
        btn_save = Button(self, "save", self.width() - 75, 2, 40, 26, "btn_standart", self.saveSettings)

        label_mealKey = Label(self, 25, 45, 100, 30, "label", "Meal key")
        label_mealKey.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.entry_mealKey = Entry(self, self.width() - 160, 40, 140, 30, "0-9", False, "entry_standart")

        label_rodKey = Label(self, 25, 90, 100, 30, "label", "Rod key")
        label_rodKey.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.entry_rodKey = Entry(self, self.width() - 160, 85, 140, 30, "0-9", False, "entry_standart")

    def closeWidow(self):
        self.entry_mealKey.clear()
        self.entry_rodKey.clear()
        self.close()

    def saveSettings(self):
        mealKey: int = -1
        rodKey: int = -1
        try:
            if int(self.entry_mealKey.text()) in range(0, 10):
                mealKey = self.entry_mealKey.text()
        except:
            pass
        try:
            if int(self.entry_rodKey.text()) in range(0, 10):
                rodKey = self.entry_rodKey.text()
        except:
            pass
        print(mealKey, rodKey)
        self.close()