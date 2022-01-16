from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys

from SearchFriend import Ui_SearchFriend
from ChatWindow import Window

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(622, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gaduGaduLabel = QtWidgets.QLabel(self.centralwidget)
        self.gaduGaduLabel.setGeometry(QtCore.QRect(0, 0, 621, 61))

        palette = self.getPalette()
        self.gaduGaduLabel.setPalette(palette)

        font = QtGui.QFont()
        font.setFamily("Jokerman")
        font.setPointSize(36)
        font.setBold(False)
        font.setWeight(50)

        self.gaduGaduLabel.setFont(font)
        self.gaduGaduLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.gaduGaduLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.addFriendButton = QtWidgets.QPushButton(self.centralwidget)
        self.addFriendButton.setGeometry(QtCore.QRect(450, 150, 171, 61))

        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)

        self.addFriendButton.setFont(font)

        self.logOutButton = QtWidgets.QPushButton(self.centralwidget)
        self.logOutButton.setGeometry(QtCore.QRect(520, 510, 93, 28))

        font.setPointSize(9)
        self.logOutButton.setFont(font)

        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(0, 220, 621, 281))

        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)

        item = QtWidgets.QListWidgetItem()
        item.setFont(font)
        self.listWidget.addItem(item)

        item = QtWidgets.QListWidgetItem()
        item.setFont(font)
        self.listWidget.addItem(item)

        item = QtWidgets.QListWidgetItem()
        item.setFont(font)
        self.listWidget.addItem(item)

        self.yourFriendsLabel = QtWidgets.QLabel(self.centralwidget)
        self.yourFriendsLabel.setGeometry(QtCore.QRect(0, 170, 171, 41))

        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)

        self.yourFriendsLabel.setFont(font)

        self.helloLabel = QtWidgets.QLabel(self.centralwidget)
        self.helloLabel.setGeometry(QtCore.QRect(10, 80, 131, 31))

        font.setPointSize(14)

        self.helloLabel.setFont(font)

        self.descriptionEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.descriptionEdit.setGeometry(QtCore.QRect(0, 111, 621, 31))

        font = QtGui.QFont()
        font.setFamily("Imprint MT Shadow")
        font.setPointSize(10)

        self.descriptionEdit.setFont(font)
        self.descriptionEdit.setAlignment(QtCore.Qt.AlignCenter)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 622, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.listWidget.itemDoubleClicked.connect(self.openChat)

        self.addFriendButton.clicked.connect(self.addFriend)

        self.logOutButton.clicked.connect(self.askBeforeLogOut)

        self.chatWindows = []


    def openChat(self, friendLogin):
        print(friendLogin.text())
        # TODO wyskakuje okienko z chatem
        self.openChatWindow(friendLogin.text())
        

    def openChatWindow(self, user):
        window = Window(user)
        window.exec()
        self.chatWindows.append(window)


    def addFriend(self):
        print("add friend")
        # TODO szukanie znajomych po loginie
        self.openSearchFriend()


    def openSearchFriend(self):
        self.window = QtWidgets.QMainWindow()   
        self.ui = Ui_SearchFriend()
        self.ui.setupUi(self.window)
        self.window.show()
        

    def askBeforeLogOut(self):
        msg = QMessageBox()
        msg.setWindowTitle("Log out")
        msg.setText("Do You want to log out?")

        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)

        msg.buttonClicked.connect(self.popup_button)

        x = msg.exec_()


    def popup_button(self, i):
        if i.text() == "&Yes":
            self.LogOut()


    def LogOut(self):
        QtWidgets.qApp.quit()


    def getPalette(self):
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 170, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 170, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)

        return palette


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Gadu Gadu"))
        self.gaduGaduLabel.setText("Gadu Gadu")
        self.yourFriendsLabel.setText("Your friends:")
        self.helloLabel.setText(_translate("MainWindow", "Hello {login}! "))
        self.descriptionEdit.setText(_translate("MainWindow", "My description"))
        self.addFriendButton.setText("Add a friend")
        self.logOutButton.setText("Log out")

        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)

        item = self.listWidget.item(0)
        item.setText(_translate("MainWindow", "Osoba 1"))

        item = self.listWidget.item(1)
        item.setText(_translate("MainWindow", "Osoba 2"))

        item = self.listWidget.item(2)
        item.setText(_translate("MainWindow", "Osoba 3"))

        self.listWidget.setSortingEnabled(__sortingEnabled)


def main():

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()