from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from User import User, getUser, addFriend


class Ui_SearchFriend(object):
    def setupUi(self, SearchFriend, user):
        self.currentUser = user
        SearchFriend.setObjectName("SearchFriend")
        SearchFriend.resize(400, 252)

        self.searchButton = QtWidgets.QToolButton(SearchFriend)
        self.searchButton.setGeometry(QtCore.QRect(310, 140, 71, 41))

        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)

        self.searchButton.setFont(font)
        self.searchButton.setObjectName("searchButton")

        self.friendsLogin = QtWidgets.QLineEdit(SearchFriend)
        self.friendsLogin.setGeometry(QtCore.QRect(10, 80, 381, 41))

        self.friendsLogin.setFont(font)
        self.friendsLogin.setDragEnabled(False)
        self.friendsLogin.setClearButtonEnabled(True)
        self.friendsLogin.setObjectName("friendsLogin")

        self.errorLabel = QtWidgets.QLabel(SearchFriend)
        self.errorLabel.setGeometry(QtCore.QRect(10, 200, 361, 41))

        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.errorLabel.setPalette(palette)
        
        self.errorLabel.setFont(font)
        self.errorLabel.setText("")
        self.errorLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.errorLabel.setObjectName("errorLabel")

        self.label = QtWidgets.QLabel(SearchFriend)
        self.label.setGeometry(QtCore.QRect(10, 30, 131, 41))
        
        font.setPointSize(14)

        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(SearchFriend)
        QtCore.QMetaObject.connectSlotsByName(SearchFriend)

        self.getAllUsers()
        # self.friendAdded = False

        self.searchButton.clicked.connect(self.searchFriend)


    def searchFriend(self):
        login = self.friendsLogin.text()

        if len(login) < 5:
            self.errorLabel.setText("Login too short.")
        elif len(login) > 20:
            self.errorLabel.setText("Login too long.")

        foundFriend = getUser(login)

        if foundFriend != None:
            print("found! " + foundFriend.toString())
            print(self.currentUser.friends)
            if foundFriend.login in self.currentUser.friends:
                self.errorLabel.setText("Already Your friend")
            elif foundFriend.login == self.currentUser.login:
                self.errorLabel.setText("This is your login")
            else:
                addFriend(self.currentUser, foundFriend)
                # self.friendAdded = True
                self.errorLabel.setText("Friend added")
        else:
            self.errorLabel.setText("Login not found.")

    def getAllUsers(self):
        
        self.users = []

        with open(r"users.txt", "r") as f:
            for line in f:
                tmp = line.split()
                login, password, name = tmp[0], tmp[1], " ".join(tmp[2:])
                self.users.append([login, password, name])

        self.logins = [login for [login, _, _] in self.users]


    def retranslateUi(self, SearchFriend):
        _translate = QtCore.QCoreApplication.translate
        SearchFriend.setWindowTitle(_translate("SearchFriend", "Search a friend"))
        self.searchButton.setText("OK")
        self.friendsLogin.setText("Login")
        self.label.setText("Search a friend:")

        self.searchButton.setShortcut("Return")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    user = User("basia", "haslo1")

    SearchFriend = QtWidgets.QWidget()
    ui = Ui_SearchFriend()
    ui.setupUi(SearchFriend, user)
    SearchFriend.show()

    sys.exit(app.exec_())
