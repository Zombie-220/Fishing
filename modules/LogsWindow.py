from PyQt6 import QtWidgets, QtCore, QtGui
from time import struct_time

from modules.GlobalVariables import CSS, EXIT_ICON
from modules.SimpleComponents import WindowTitleBar, Button
from modules.header import MainWindow

class LogsWindow(QtWidgets.QMainWindow):
    logs: list = []

    def __init__(self, parent: MainWindow):
        QtWidgets.QMainWindow.__init__(self)

        self.title = "AF  |  History"
        self.icon = parent.icon

        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.icon))
        self.setFixedSize(350, 400)
        self.move(parent.pos().x() + parent.width(), parent.height() + 10)
        self.setObjectName("Window")
        self.setStyleSheet(CSS)

        windowTitle = WindowTitleBar(self)
        btn_close = Button(self, EXIT_ICON, self.width() - 28, 2, 26, 26, "btn_red", self.close)
        btn_close.setToolTip("Close window")
        btn_clear = Button(self, "Clear", self.width() - 80, 2, 50, 26, "btn_standart", self.deleteLogs)
        btn_clear.setToolTip("Clear history")

        self.__widget = QtWidgets.QWidget()
        self.__widget.setObjectName("widget")
        self.__vBox = QtWidgets.QVBoxLayout()  
        self.__vBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.__widget.setLayout(self.__vBox)

        self.__scrollArea = QtWidgets.QScrollArea(self)
        self.__scrollArea.move(2,32)
        self.__scrollArea.setFixedSize(self.width() - 4, self.height() - 34)
        self.__scrollArea.setObjectName("scrollArea")
        self.__scrollArea.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.__scrollArea.setWidgetResizable(True)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.checkLogs)
        self.timer.setInterval(500)
        self.timer.start()

    def addLog(self, time: struct_time, reasonType: str):
        objectName = f"btn_{reasonType}_log"
        if reasonType == "fish" or reasonType == "junk":
            reason = "Fish caught"
        elif reasonType == "sunken":
            reason = "Sunken treasure caught"
        elif reasonType == "treasure":
            reason = "Treasure caught"
        elif reasonType == "timeOut":
            reason = "Attempt timed out"
        elif reasonType == "start":
            reason = "Session start"
        elif reasonType == "stop":
            reason = "Session end"
        elif reasonType == "timeError":
            reason = "Waiting time is up"

        btn = Button(self, f"{time.tm_hour:02}:{time.tm_min:02}:{time.tm_sec:02}  |  {reason}", 0, 0, 0, 0, objectName)
        self.__vBox.addWidget(btn)
        self.__scrollArea.setWidget(self.__widget)

    def checkLogs(self):
        if len(self.logs) != 0:
            try:
                for i in range(len(self.logs)):
                    self.addLog(self.logs[i][0], self.logs[i][1])
                    self.logs.pop(i)
            except: pass
        self.timer.start()

    def deleteLogs(self):
        while self.__vBox.itemAt(0):
            self.__vBox.removeWidget(self.__vBox.itemAt(0).widget())