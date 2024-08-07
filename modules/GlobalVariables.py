from PyQt6 import QtGui, QtCore, QtWidgets
import sys, os

app = QtWidgets.QApplication(sys.argv)

APP_ICON = QtGui.QPixmap(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}\images\icons\APP_ICON.png').scaled(
                        30, 30, transformMode = QtCore.Qt.TransformationMode.SmoothTransformation)
SETTING_ICON = QtGui.QIcon(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}\images\icons\SETTING_ICON.png')
EXIT_ICON = QtGui.QIcon(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}\images\icons\EXIT_ICON.png')
LOGS_ICON = QtGui.QIcon(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}\images\icons\LOGS_ICON.png')

CSS = '''
    * {
        color: rgb(240, 240, 240);
        font-size: 14px;
    }
    #widget {
        background-color: rgba(0,0,0,0);
    }

    #MainWindow, #TitleBar, #Window, QToolTip, #btn_fish_log, QComboBox, QComboBox QAbstractItemView, QComboBox::drop-down {
        background-color: rgb(21, 21, 21);
        border: 1px solid rgb(145, 145, 145);
    }
    QComboBox::drop-down {
        image: url(./images/icons/DOWN_ARROW.png);
        width: 20px;
        height: 20px;
    }
    QToolTip {
        font-size: 12px;
    }

    
    #btn_standart {
        background-color: rgba(0, 65, 129, 1);
        border: 1px solid rgb(145, 145, 145);
    }
    #btn_standart::hover {
        background-color: rgba(0, 65, 129, 0.7);
    }
    #btn_standart::pressed {
        background-color: rgba(0, 65, 129, 0.5);
    }

    #btn_red, #btn_stop_log, #btn_stop {
        background-color: rgba(57, 21, 21, 1);
        border: 1px solid rgb(145, 0, 0);
    }
    #btn_red::hover, #btn_stop::hover {
        background-color: rgba(57, 21, 21, 0.7);
    }
    #btn_red::pressed, #btn_stop::pressed {
        background-color: rgba(57, 21, 21, 0.5);
    }

    #entry_standart {
        background-color: rgba(21, 21, 21, 1);
        border: 1px solid rgba(0, 65, 129, 1);
        selection-background-color: rgba(0, 65, 129, 0.6);
    }
    #entry_red {
        background-color: rgba(21, 21, 21, 1);
        border: 1px solid rgb(145, 0, 0);
        selection-background-color: rgba(145, 0, 0, 0.6);
    }
    

    #scrollArea {
        background-color: rgba(0,0,0,0);
        border: 0px;
    }
    QScrollBar:vertical {
        background-color: rgba(0, 0, 0, 0);
        width: 7px;
    }
    QScrollBar::handle:vertical {
        background-color: rgba(0, 65, 129, 1);
        border: 1px solid rgb(145, 145, 145);
    }
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background-color: rgba(0, 0, 0, 1);
    }
    

    #btn_start_log {
        background-color: rgb(20, 72, 21);
        border: 1px solid rgb(0, 145, 0);
    }
    #btn_treasure_log {
        background-color: rgba(0, 0, 0, 0);
        border: 1px solid rgb(178, 134, 22);
    }
    #btn_sunken_log {
        background-color: rgb(12, 15, 22);
        border: 1px solid rgb(67, 67, 178);
    }
    #btn_timeError_log {
        background-color: rgb(41, 9, 41);
        border: 1px solid rgb(127, 0, 127);
    }
    #btn_consumeMeal_log, #btn_consumePotion_log {
        background-color: rgba(0, 65, 129, 0.3);
        border: 1px solid rgb(145, 145, 145);
    }
'''