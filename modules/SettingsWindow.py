from PyQt6 import QtWidgets, QtGui, QtCore

from modules.header import MainWindow
from modules.SimpleComponents import WindowTitleBar, Button, Entry, Label
from modules.GlobalVariables import CSS, EXIT_ICON

import os, sys, json

class SettingsWindow(QtWidgets.QMainWindow):
    rodKey: int = 0
    mealKey: int = 9
    potionKey: int = 8
    useMeal: bool = False
    usePotion: bool = False

    def __init__(self, parent: MainWindow):
        QtWidgets.QWidget.__init__(self)

        self.title = "AF  |  Settings"
        self.icon = parent.icon

        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.icon))
        self.setFixedSize(350, 175)
        self.move(parent.pos().x() - 60, parent.height() + 10)
        self.setObjectName("Window")
        self.setStyleSheet(CSS)

        windowTitle = WindowTitleBar(self)
        btn_close = Button(self, EXIT_ICON, self.width() - 28, 2, 26, 26, "btn_red", self.close)
        btn_close.setToolTip("Close window")
        btn_cancel = Button(self, "Cancel", self.width() - 80, 2, 50, 26, "btn_red", self.clearEntrys)
        btn_cancel.setToolTip("Cancel all changes")
        btn_save = Button(self, "Save", self.width() - 132, 2, 50, 26, "btn_standart", self.saveChanges)
        btn_save.setToolTip("Save changes")    

        self.openDataBase()

        grid = QtWidgets.QGridLayout()
        label = QtWidgets.QLabel(self)
        grid.setColumnMinimumWidth(1, 100)

        label_rodKey = Label(self, 0, 0, 0, 0, "label", "Rod key")
        label_rodKey.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)    
        self.__entry_rodKey = Entry(self, 0, 0, 0, 0, f"0-9, default is {self.rodKey}", False, "entry_standart")
        grid.addWidget(label_rodKey, 0, 0)
        grid.addWidget(self.__entry_rodKey, 0, 1, 1, 2)

        label_mealKey = Label(self, 0, 0, 0, 0, "label", "Meal key")
        label_mealKey.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.__button_useMeal = Button(self, "Use meal", 0, 0, 0, 0, "btn_red", self.changeMealFlag)
        self.__entry_mealKey = Entry(self, 0, 0, 0, 0, f"0-9, default is {self.mealKey}", False, "entry_standart")
        grid.addWidget(label_mealKey, 1, 0)
        grid.addWidget(self.__button_useMeal, 1, 1)
        grid.addWidget(self.__entry_mealKey, 1, 2)

        label_potionKey = Label(self, 0, 0, 0, 0, "lable", "Potion key")
        label_potionKey.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.__button_usePotion = Button(self, "Use potion", 0, 0, 0, 0, "btn_red", self.changePotionFlag)
        self.__entry_potionKey = Entry(self, 0, 0, 0, 0, f"0-9, default is {self.potionKey}", False, "entry_standart")
        grid.addWidget(label_potionKey, 2, 0)
        grid.addWidget(self.__button_usePotion, 2, 1)
        grid.addWidget(self.__entry_potionKey, 2, 2)

        self.__entry_potionDuration = Entry(self, 0, 0, 0, 0, "potion duration", False, "entry_standart")
        grid.addWidget(self.__entry_potionDuration, 3, 0, 1, 3)

        label.setFixedSize(self.width() - 4, self.height() - 34)
        label.move(2, 32)
        label.setLayout(grid)

    def changeMealFlag(self):
        self.useMeal = not self.useMeal
        if self.useMeal:
            self.__button_useMeal.setObjectName("btn_standart")
        else:
            self.__button_useMeal.setObjectName("btn_red")
        self.setStyleSheet(CSS)
        print(self.useMeal)

    def changePotionFlag(self):
        self.usePotion = not self.usePotion
        if self.usePotion:
            self.__button_usePotion.setObjectName("btn_standart")
        else:
            self.__button_usePotion.setObjectName("btn_red")
        self.setStyleSheet(CSS)
        print(self.usePotion)

    def clearEntrys(self):
        self.__entry_rodKey.clear()
        self.__entry_mealKey.clear()
        self.__entry_potionKey.clear()
        self.close()

    def saveChanges(self):
        if self.__entry_rodKey.text() != "":
            try: newRodKey = float(self.__entry_rodKey.text())
            except: return
            if (newRodKey not in range(0, 10)) or (int(newRodKey % 1 * 10) != 0): return
        else:
            newRodKey = self.rodKey
        self.rodKey = int(newRodKey)
        self.__entry_rodKey.setPlaceholderText(f"0-9, default is {self.rodKey}")

        if self.__entry_mealKey.text() != "":
            try: newMealKey = float(self.__entry_mealKey.text())
            except: return
            if (newMealKey not in range(0, 10)) or (int(newMealKey % 1 * 10) != 0): return
        else:
            newMealKey = self.mealKey
        self.mealKey = int(newMealKey)
        self.__entry_mealKey.setPlaceholderText(f"0-9, default is {self.mealKey}")
        
        if self.__entry_potionKey.text() != "":
            try: newPotionKey = float(self.__entry_potionKey.text())
            except: return
            if (newPotionKey not in range(0, 10)) or (int(newPotionKey % 1 * 10) != 0): return
        else:
            newPotionKey = self.potionKey
        self.potionKey = int(newPotionKey)
        self.__entry_potionKey.setPlaceholderText(f"0-9, default is {self.potionKey}")
        
        self.clearEntrys()

    def openDataBase(self):
        if not os.path.isfile(Rf'{os.path.abspath(os.path.dirname(sys.argv[0]))}/DB.json'):
            print("Файл не существует")
        else:
            file = open("DB.json", "r")
            data = json.loads(file.read())

            self.rodKey = data["rodKey"]
            self.mealKey = data["mealKey"]
            self.potionKey = data["potionKey"]

            print(data['useMeal'])
            print(data['usePotion'])
            print(data['potionDuration'])