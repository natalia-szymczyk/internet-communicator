from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys

from User import User, getUser
from SearchFriend import Ui_SearchFriend
from ChatWindow import Ui_ChatWindow

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, user):
        self.currentUser = user
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

        for i in range(len(user.friends)):
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
        self.helloLabel.setGeometry(QtCore.QRect(10, 80, 231, 31))

        font.setPointSize(14)

        self.helloLabel.setFont(font)

        self.descriptionEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.descriptionEdit.setGeometry(QtCore.QRect(0, 111, 631, 31))

        font = QtGui.QFont()
        font.setFamily("Imprint MT Shadow")
        font.setPointSize(10)

        self.descriptionEdit.setFont(font)
        self.descriptionEdit.setAlignment(QtCore.Qt.AlignCenter)

        self.descriptionButton = QtWidgets.QPushButton(self.centralwidget)
        self.descriptionButton.setGeometry(QtCore.QRect(540, 111, 81, 31))

        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)

        self.descriptionButton.setFont(font)

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

        self.descriptionButton.clicked.connect(self.changeDescription)

        self.chatWindows = []

    def changeDescription(self):
        description = self.descriptionEdit.text()
        self.currentUser.updateDescription(description)


    def openChat(self, element):
        start = '('
        end = ')'
        friendsString = element.text()
        friendLogin = friendsString[friendsString.find(start)+len(start):friendsString.rfind(end)]
        friend = getUser(friendLogin)
        self.openChatWindow(friend)
        

    def openChatWindow(self, friend):
        self.window = QtWidgets.QWidget()
        self.ui = Ui_ChatWindow()
        self.ui.setupUi(self.window, self.currentUser, friend)
        self.window.show()
        self.chatWindows.append(self.window)


    def addFriend(self):
        self.openSearchFriend()


    def openSearchFriend(self):
        # before = self.currentUser.friends
        # print(f"before {before}")

        self.window = QtWidgets.QMainWindow()   
        self.ui = Ui_SearchFriend()
        self.ui.setupUi(self.window, self.currentUser)
        self.window.show()

        # TODO update friends list ??

        # after = self.currentUser.friends
        # print(f"after {after}")

        # print(f"bool:  {self.ui.friendAdded}")

        # if before != after:
        #     self.updateFriendsList()

        

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
            self.logOut()


    def logOut(self):
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
        self.helloLabel.setText(_translate("MainWindow", f"Hello {self.currentUser.name}! "))
        self.descriptionEdit.setText(_translate("MainWindow", self.currentUser.description))
        self.addFriendButton.setText("Add a friend")
        self.logOutButton.setText("Log out")
        self.descriptionButton.setText("Change")

        self.updateFriendsList()

    def updateFriendsList(self):
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)

        for i in range(len(self.currentUser.friends)):
            print(self.currentUser.friends[i])

            item = self.listWidget.item(i)
            friend = getUser(self.currentUser.friends[i])
            item.setText(friend.toString())

        self.listWidget.setSortingEnabled(__sortingEnabled)


def main():

    user = User("basia", "haslo1")

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, user)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()