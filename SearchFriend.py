from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class Ui_SearchFriend(object):
    def setupUi(self, SearchFriend):
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

        self.searchButton.clicked.connect(self.searchFriend)


    def searchFriend(self):
        login = self.friendsLogin.text()
        print("searching " + login )

        if len(login) < 5:
            self.errorLabel.setText("Login too short.")
        
        found = True 
        # TODO szukanie znajomych

        if not found:
            self.errorLabel.setText("Login not found.")



    def retranslateUi(self, SearchFriend):
        _translate = QtCore.QCoreApplication.translate
        SearchFriend.setWindowTitle(_translate("SearchFriend", "Search a friend"))
        self.searchButton.setText("OK")
        self.friendsLogin.setText("Login")
        self.label.setText("Search a friend:")

        self.searchButton.setShortcut("Return")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    SearchFriend = QtWidgets.QWidget()
    ui = Ui_SearchFriend()
    ui.setupUi(SearchFriend)
    SearchFriend.show()

    sys.exit(app.exec_())
