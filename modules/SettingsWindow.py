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
    timeForTry: int = 22.5
    mealTimer: int = 300
    potionTimer: int = 300

    def __init__(self, parent: QtWidgets.QMainWindow):
        super().__init__()

        self.title = "AF  |  Settings"
        self.icon = parent.icon

        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.icon))
        self.setFixedSize(360, 250)
        self.move(parent.pos().x() - 75, parent.height() + 10)
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
        label_mealTimer = Label(self, 0, 0, 0, 0, "label", "Meal timer")
        label_mealTimer.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.__entry_mealTimer = Entry(self, 0, 0, 0, 0, "EMPTY", False, "entry_standart")
        grid.addWidget(label_mealKey, 1, 0)
        grid.addWidget(self.__button_useMeal, 1, 1)
        grid.addWidget(self.__entry_mealKey, 1, 2)
        grid.addWidget(label_mealTimer, 2, 0)
        grid.addWidget(self.__entry_mealTimer, 2, 1, 1, 2)

        label_potionKey = Label(self, 0, 0, 0, 0, "lable", "Potion key")
        label_potionKey.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.__button_usePotion = Button(self, "Use potion", 0, 0, 0, 0, "btn_red", self.changePotionFlag)
        self.__entry_potionKey = Entry(self, 0, 0, 0, 0, "EMPTY", False, "entry_standart")
        label_potionTimer = Label(self, 0, 0, 0, 0, "label", "Potion timer")
        label_potionTimer.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.__entry_potionTimer = Entry(self, 0, 0, 0, 0, "EMPTY", False, "entry_standart")
        grid.addWidget(label_potionKey, 3, 0)
        grid.addWidget(self.__button_usePotion, 3, 1)
        grid.addWidget(self.__entry_potionKey, 3, 2)
        grid.addWidget(label_potionTimer, 4, 0)
        grid.addWidget(self.__entry_potionTimer, 4, 1, 1, 2)

        label_seaChoise = Label(self, 0, 0, 0, 0, "label", "Sea choise")
        label_seaChoise.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.__sea_combo = QtWidgets.QComboBox(self)
        self.__sea_combo.addItems(["Normal sea", "Dark sea"])
        grid.addWidget(label_seaChoise, 5, 0)
        grid.addWidget(self.__sea_combo, 5, 1, 1, 2)

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
        self.__entry_mealTimer.clear()
        self.__entry_potionTimer.clear()

        self.__entry_rodKey.setObjectName("entry_standart")
        self.__entry_mealKey.setObjectName("entry_standart")
        self.__entry_potionKey.setObjectName("entry_standart")
        self.__entry_mealTimer.setObjectName("entry_standart")
        self.__entry_potionTimer.setObjectName("entry_standart")
        self.setStyleSheet(CSS)

        if self.timeForTry == 22.5: self.__sea_combo.setCurrentIndex(0)
        elif self.timeForTry == 30: self.__sea_combo.setCurrentIndex(1)

        self.close()

    def checkEntry(self, variable: int|str, entry: Entry):
        newVariable = entry.text().lower()
        if (newVariable in ['1','2','3','4','5','6','7','8','9','0']) or (entry == self.__entry_potionKey and newVariable == 'e') or (newVariable == ''):
            if newVariable in ['1','2','3','4','5','6','7','8','9','0']:
                newVariable = int(newVariable)
            elif newVariable == '':
                newVariable = variable
            entry.setObjectName("entry_standart")
            if entry == self.__entry_potionKey: entry.setPlaceholderText(f"0-9 or E, default is {newVariable}")
            else: entry.setPlaceholderText(f"0-9, default is {newVariable}")
            self.setStyleSheet(CSS)
            return newVariable, True
        else:
            entry.setObjectName("entry_red")
            self.setStyleSheet(CSS)
            return variable, False
        
    def checkEntryWithTime(self, variable: int|str, entry: Entry):
        newValue = entry.text()
        try:
            newValue = int(newValue)
            entry.setObjectName("entry_standart")
            boolResult = True
        except:
            if newValue == "":
                newValue = variable
                boolResult = True
                entry.setObjectName("entry_standart")
            else:
                entry.setObjectName("entry_red")
                self.setStyleSheet(CSS)
                newValue = variable
                boolResult = False
        self.setStyleSheet(CSS)
        entry.setPlaceholderText(f"{newValue} seconds")
        return newValue, boolResult

    def saveChanges(self) -> None:
        check1 = self.checkEntry(self.rodKey, self.__entry_rodKey)
        check2 = self.checkEntry(self.mealKey, self.__entry_mealKey)
        check3 = self.checkEntry(self.potionKey, self.__entry_potionKey)
        check4 = self.checkEntryWithTime(self.mealTimer, self.__entry_mealTimer)
        check5 = self.checkEntryWithTime(self.potionTimer, self.__entry_potionTimer)

        self.rodKey = check1[0]
        self.mealKey = check2[0]
        self.potionKey = check3[0]
        self.mealTimer = check4[0]
        self.potionTimer = check5[0]
        sea = self.__sea_combo.currentText()
        if sea == "Normal sea": self.timeForTry = 22.5
        elif sea == "Dark sea": self.timeForTry = 30

        if check1[1] and check2[1] and check3[1] and check4[1] and check5[1]:
            self.clearEntrys()

            newDBobject = {
                "rodKey": self.rodKey,
                "mealKey": self.mealKey,
                "potionKey": self.potionKey,
                "useMeal": self.useMeal,
                "usePotion": self.usePotion,
                "mealTimer": self.mealTimer,
                "potionTimer": self.potionTimer,
                "timeForTry": self.timeForTry
            }

            with open('DB.json', 'w') as file:
                json.dump(newDBobject, file)

    def readDataBase(self) -> None:
        file = open("DB.json", "r")
        data = json.loads(file.read())

        self.rodKey = data["rodKey"]
        self.mealKey = data["mealKey"]
        self.potionKey = data["potionKey"]
        self.useMeal = data["useMeal"]
        self.usePotion = data["usePotion"]
        self.mealTimer = data["mealTimer"]
        self.potionTimer = data["potionTimer"]
        self.timeForTry = data["timeForTry"]

        self.__entry_rodKey.setPlaceholderText(f"0-9, default is {self.rodKey}")
        self.__entry_mealKey.setPlaceholderText(f"0-9, default is {self.mealKey}")
        self.__entry_potionKey.setPlaceholderText(f"0-9 or E, default is {self.potionKey}")
        if self.useMeal: self.__button_useMeal.setObjectName("btn_standart")
        if self.usePotion: self.__button_usePotion.setObjectName("btn_standart")
        self.__entry_mealTimer.setPlaceholderText(f"{self.mealTimer} seconds")
        self.__entry_potionTimer.setPlaceholderText(f"{self.potionTimer} seconds")
        if self.timeForTry == 22.5: self.__sea_combo.setCurrentIndex(0)
        elif self.timeForTry == 30: self.__sea_combo.setCurrentIndex(1)