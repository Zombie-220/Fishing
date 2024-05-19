from PyQt6 import QtWidgets, QtGui, QtCore
import json

from modules.SimpleComponents import WindowTitleBar, Button, Entry, Label
from modules.GlobalVariables import CSS, EXIT_ICON

class SettingsWindow(QtWidgets.QMainWindow):
    rodKey: int = 0
    mealKey: int = 9
    potionKey: int|str = 8
    useMeal: bool = False
    usePotion: bool = False
    checkTime: int = 300

    allOK: bool = True

    def __init__(self, parent: QtWidgets.QMainWindow):
        super().__init__()

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

        grid = QtWidgets.QGridLayout()
        label = QtWidgets.QLabel(self)
        grid.setColumnMinimumWidth(1, 100)

        label_rodKey = Label(self, 0, 0, 0, 0, "label", "Rod key")
        label_rodKey.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)    
        self.__entry_rodKey = Entry(self, 0, 0, 0, 0, "EMPTY", False, "entry_standart")
        grid.addWidget(label_rodKey, 0, 0)
        grid.addWidget(self.__entry_rodKey, 0, 1, 1, 2)

        label_mealKey = Label(self, 0, 0, 0, 0, "label", "Meal key")
        label_mealKey.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.__button_useMeal = Button(self, "Use meal", 0, 0, 0, 0, "btn_red", self.changeMealFlag)
        self.__entry_mealKey = Entry(self, 0, 0, 0, 0, "EMPTY", False, "entry_standart")
        grid.addWidget(label_mealKey, 1, 0)
        grid.addWidget(self.__button_useMeal, 1, 1)
        grid.addWidget(self.__entry_mealKey, 1, 2)

        label_potionKey = Label(self, 0, 0, 0, 0, "lable", "Potion key")
        label_potionKey.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.__button_usePotion = Button(self, "Use potion", 0, 0, 0, 0, "btn_red", self.changePotionFlag)
        self.__entry_potionKey = Entry(self, 0, 0, 0, 0, "EMPTY", False, "entry_standart")
        grid.addWidget(label_potionKey, 2, 0)
        grid.addWidget(self.__button_usePotion, 2, 1)
        grid.addWidget(self.__entry_potionKey, 2, 2)

        label_potionDuration = Label(self, 0, 0, 0, 0, "label", "Eat | drink timer")
        self.__entry_potionDuration = Entry(self, 0, 0, 0, 0, "EMPTY", False, "entry_standart")
        grid.addWidget(label_potionDuration, 3, 0)
        grid.addWidget(self.__entry_potionDuration, 3, 1, 1, 2)

        label.setFixedSize(self.width() - 4, self.height() - 34)
        label.move(2, 32)
        label.setLayout(grid)

        self.readDataBase()

    def changeMealFlag(self) -> None:
        self.useMeal = not self.useMeal
        if self.useMeal: self.__button_useMeal.setObjectName("btn_standart")
        else: self.__button_useMeal.setObjectName("btn_red")
        self.setStyleSheet(CSS)

    def changePotionFlag(self) -> None:
        self.usePotion = not self.usePotion
        if self.usePotion: self.__button_usePotion.setObjectName("btn_standart")
        else: self.__button_usePotion.setObjectName("btn_red")
        self.setStyleSheet(CSS)

    def clearEntrys(self) -> None:
        self.__entry_rodKey.clear()
        self.__entry_mealKey.clear()
        self.__entry_potionKey.clear()
        self.__entry_potionDuration.clear()

        self.__entry_rodKey.setObjectName("entry_standart")
        self.__entry_mealKey.setObjectName("entry_standart")
        self.__entry_potionKey.setObjectName("entry_standart")
        self.__entry_potionDuration.setObjectName("entry_standart")
        self.setStyleSheet(CSS)
        self.close()

    def checkEntry(self, variable: int|str, entry: Entry):
        newVariable = entry.text().lower()
        if (newVariable in ['1','2','3','4','5','6','7','8','9','0']) or (entry == self.__entry_potionKey and newVariable == 'e') or (newVariable == ''):
            if newVariable in ['1','2','3','4','5','6','7','8','9','0']:
                newVariable = int(newVariable)
            elif newVariable == '':
                newVariable = variable
            entry.setObjectName("entry_standart")
            entry.setPlaceholderText(f"0-9, default is {newVariable}")
            self.setStyleSheet(CSS)
            return newVariable, True
        else:
            entry.setObjectName("entry_red")
            self.setStyleSheet(CSS)
            return variable, False

    def saveChanges(self) -> None:
        check1 = self.checkEntry(self.rodKey, self.__entry_rodKey)
        check2 = self.checkEntry(self.mealKey, self.__entry_mealKey)
        check3 = self.checkEntry(self.potionKey, self.__entry_potionKey)

        self.rodKey = check1[0]
        self.mealKey = check2[0]
        self.potionKey = check3[0]

        newPotionDuration = self.__entry_potionDuration.text()
        try:
            newPotionDuration = int(newPotionDuration)
            self.allOK = True
        except:
            if newPotionDuration == "":
                newPotionDuration = self.checkTime
                self.allOK = True
            else:
                self.__entry_potionDuration.setObjectName("entry_red")
                self.setStyleSheet(CSS)
                newPotionDuration = self.checkTime
                self.allOK = False
                return
        self.__entry_potionDuration.setObjectName("entry_standart")
        self.setStyleSheet(CSS)

        self.checkTime = newPotionDuration
        self.__entry_potionDuration.setPlaceholderText(f"{self.checkTime} seconds")
        
        if self.allOK and check1[1] and check2[1] and check3[1]:
            self.clearEntrys()

            newDBobject = {
                "rodKey": self.rodKey,
                "mealKey": self.mealKey,
                "potionKey": self.potionKey,
                "useMeal": self.useMeal,
                "usePotion": self.usePotion,
                "checkTime": self.checkTime
            }

            with open('DB.json', 'w') as file:
                json.dump(newDBobject, file)

    def readDataBase(self) -> None:
        file = open("DB.json", "r")
        data = json.loads(file.read())

        self.rodKey = data["rodKey"]
        self.__entry_rodKey.setPlaceholderText(f"0-9, default is {self.rodKey}")
        self.mealKey = data["mealKey"]
        self.__entry_mealKey.setPlaceholderText(f"0-9, default is {self.mealKey}")
        self.potionKey = data["potionKey"]
        self.__entry_potionKey.setPlaceholderText(f"0-9, default is {self.potionKey}")
        self.useMeal = data["useMeal"]
        if self.useMeal:
            self.__button_useMeal.setObjectName("btn_standart")
        self.usePotion = data["usePotion"]
        if self.usePotion:
            self.__button_usePotion.setObjectName("btn_standart")
        self.checkTime = data["checkTime"]
        self.__entry_potionDuration.setPlaceholderText(f"{self.checkTime} seconds")