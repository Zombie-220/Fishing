from PyQt6 import QtWidgets, QtGui

class MainWindow(QtWidgets.QMainWindow):
    title: str = None
    icon: QtGui.QPixmap = None

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

    def windowShouldClose(self):
        pass
    