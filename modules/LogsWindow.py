from PyQt6 import QtWidgets, QtCore, QtGui
from time import struct_time

from modules.GlobalVariables import CSS, EXIT_ICON
from modules.SimpleComponents import WindowTitleBar, Button
from modules.header import MainWindow

class LogsWindow(QtWidgets.QMainWindow):
    logs: list = []

    def __init__(self, parent: MainWindow):
        QtWidgets.QMainWindow.__init__(self)

        self.title = "AF  |  Logs"
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
        btn_clear = Button(self, "Clear", self.width() - 70, 2, 40, 26, "btn_standart", self.deleteLogs)

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

    def addLog(self, time: struct_time, type: str):
        objectName = f"btn_{type}_log"
        if type == "fish" or type == "junk":
            reason = "Fish caught"
        elif type == "sunken":
            reason = "Sunken treasure caught"
        elif type == "treasure":
            reason = "Treasure caught"
        elif type == "timeOut":
            reason = "Attempt timed out"
        elif type == "start":
            reason = "Session start"
        elif type == "stop":
            reason = "Session end"

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