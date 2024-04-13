from PyQt6 import QtWidgets, QtGui, QtCore

from modules.header import MainWindow
from modules.SimpleComponents import WindowTitleBar, Button, Entry, Label
from modules.GlobalVariables import CSS, EXIT_ICON

class SettingsWindow(QtWidgets.QMainWindow):
    rodKey: int = 6

    def __init__(self, parent: MainWindow):
        QtWidgets.QWidget.__init__(self)

        self.title = "AF  |  Settings"
        self.icon = parent.icon

        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.icon))
        self.setFixedSize(300, 125)
        self.move(parent.pos().x(), parent.height() + 10)
        self.setObjectName("Window")
        self.setStyleSheet(CSS)

        windowTitle = WindowTitleBar(self)
        btn_close = Button(self, EXIT_ICON, self.width() - 28, 2, 26, 26, "btn_red", self.close)
        btn_close.setToolTip("Close window")
        btn_cancel = Button(self, "Cancel", self.width() - 80, 2, 50, 26, "btn_red", self.cancelChanges)
        btn_cancel.setToolTip("Cancel all changes")
        btn_save = Button(self, "Save", self.width() - 132, 2, 50, 26, "btn_standart", self.saveChanges)
        btn_save.setToolTip("Save changes")

        label_rodKey = Label(self, 25, 90, 100, 30, "label", "Rod key")
        label_rodKey.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.__entry_rodKey = Entry(self, self.width() - 160, 85, 140, 30, f"0-9, default is {self.rodKey}", False, "entry_standart")

    def cancelChanges(self):
        self.__entry_rodKey.clear()
        self.close()

    def saveChanges(self):
        if self.__entry_rodKey.text() != "":
            try: newRodKey = float(self.__entry_rodKey.text())
            except: return
            if (newRodKey not in range(0, 10)) or (int(newRodKey % 1 * 10) != 0): return
        else:
            newRodKey = self.__entry_rodKey
        self.rodKey = int(newRodKey)
        self.__entry_rodKey.setPlaceholderText(f"0-9, default is {self.rodKey}")
        self.close()
        
        # save to DB