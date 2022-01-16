from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class Ui_LoginPage(object):
    def setupUi(self, LoginPage):
        LoginPage.setObjectName("LoginPage")
        LoginPage.resize(342, 466)
        self.centralwidget = QtWidgets.QWidget(LoginPage)
        self.centralwidget.setObjectName("centralwidget")

        self.label1 = QtWidgets.QLabel(self.centralwidget)
        self.label1.setGeometry(QtCore.QRect(0, 40, 341, 51))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(24)
        self.label1.setFont(font)
        self.label1.setAlignment(QtCore.Qt.AlignCenter)
        self.label1.setObjectName("label_1")

        self.nameInputUp = QtWidgets.QLineEdit(self.centralwidget)
        self.nameInputUp.setGeometry(QtCore.QRect(40, 90, 261, 22))
        self.nameInputUp.setClearButtonEnabled(True)
        self.nameInputUp.setObjectName("name_input")

        self.loginInputUp = QtWidgets.QLineEdit(self.centralwidget)
        self.loginInputUp.setGeometry(QtCore.QRect(40, 120, 261, 22))
        self.loginInputUp.setClearButtonEnabled(True)
        self.loginInputUp.setObjectName("login_input")

        self.passwordInputUp = QtWidgets.QLineEdit(self.centralwidget)
        self.passwordInputUp.setGeometry(QtCore.QRect(40, 150, 261, 22))
        self.passwordInputUp.setAutoFillBackground(False)
        self.passwordInputUp.setClearButtonEnabled(True)
        self.passwordInputUp.setObjectName("password_input")
        self.passwordInputUp.setEchoMode(QtWidgets.QLineEdit.Password)

        self.signUpButton = QtWidgets.QPushButton(self.centralwidget)
        self.signUpButton.setGeometry(QtCore.QRect(40, 180, 261, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        self.signUpButton.setFont(font)
        self.signUpButton.setObjectName("sign_up_button")

        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(0, 240, 341, 51))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(24)
        self.label2.setFont(font)
        self.label2.setAlignment(QtCore.Qt.AlignCenter)
        self.label2.setObjectName("label_2")

        self.loginInputIn = QtWidgets.QLineEdit(self.centralwidget)
        self.loginInputIn.setGeometry(QtCore.QRect(40, 300, 261, 22))
        self.loginInputIn.setClearButtonEnabled(True)
        self.loginInputIn.setObjectName("login_input_2")

        self.passwordInputIn = QtWidgets.QLineEdit(self.centralwidget)
        self.passwordInputIn.setGeometry(QtCore.QRect(40, 330, 261, 22))
        self.passwordInputIn.setAutoFillBackground(False)
        self.passwordInputIn.setClearButtonEnabled(True)
        self.passwordInputIn.setObjectName("password_input_2")
        self.passwordInputIn.setEchoMode(QtWidgets.QLineEdit.Password)

        self.signInButton = QtWidgets.QPushButton(self.centralwidget)
        self.signInButton.setGeometry(QtCore.QRect(40, 360, 261, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        self.signInButton.setFont(font)
        self.signInButton.setObjectName("sing_in_button")
        
        self.errorLabel = QtWidgets.QLabel(self.centralwidget)
        self.errorLabel.setGeometry(QtCore.QRect(10, 5, 321, 31))
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
        font = QtGui.QFont()
        font.setPointSize(10)
        self.errorLabel.setFont(font)
        self.errorLabel.setText("")
        self.errorLabel.setObjectName("errorLabel")

        LoginPage.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(LoginPage)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 342, 26))
        self.menubar.setObjectName("menubar")
        LoginPage.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(LoginPage)
        self.statusbar.setObjectName("statusbar")
        LoginPage.setStatusBar(self.statusbar)

        self.retranslateUi(LoginPage)
        QtCore.QMetaObject.connectSlotsByName(LoginPage)

        self.signInButton.clicked.connect(self.signInCheck)

        self.signUpButton.clicked.connect(self.signUpCheck)


    def signUpCheck(self):
        print("check sign up " + " name: " + self.nameInputUp.text() + " login: " + self.loginInputUp.text() + " password: " + self.passwordInputUp.text())

        if self.passwordCheck(self.passwordInputUp.text()) and self.loginCheck(self.loginInputUp.text()):
            self.signUp()
        # else:
        #     self.errorLabel.setText("Wrong data")


    def passwordCheck(self, password):
        if len(password) < 5:
            self.errorLabel.setText("Password too short")
            return False
        elif len(password) > 20:
            self.errorLabel.setText("Password too long.")
            return False
        
        return True

    def loginCheck(self, login):
        if len(login) < 5:
            self.errorLabel.setText("Login too short")
            return False
        elif len(login) > 20:
            self.errorLabel.setText("Login too long.")
            return False

        available = True
        # TODO sprawdzanie czy login zajety

        if available == False:
            self.errorLabel.setText("Login not available.")
            return False

        return True


    def signUp(self):
        print("ok to sign up")
        # TODO rejstracja uzytkownika


    def signInCheck(self):
        print("checking sign in" + " login: " + self.loginInputIn.text() + " password: " + self.passwordInputIn.text())

        correctData = True
        # TODO sprawdzanie czy dane poprawne 

        if correctData:
            self.signIn()
        else:
            self.errorLabel.setText("Wrong data.")


    def signIn(self):
        print("ok to sign in")
        # TODO logowanie


    def retranslateUi(self, LoginPage):
        _translate = QtCore.QCoreApplication.translate
        LoginPage.setWindowTitle(_translate("LoginPage", "Gadu Gadu"))
        self.label1.setText("Need an account?")
        self.loginInputUp.setText("Login")
        self.passwordInputUp.setText("Password")
        self.signUpButton.setText("Sign up")
        self.label2.setText("Already a user?")
        self.loginInputIn.setText("Login")
        self.signInButton.setText("Sign in")
        self.passwordInputIn.setText("Password")
        self.nameInputUp.setText("Name")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    LoginPage = QtWidgets.QMainWindow()
    ui = Ui_LoginPage()
    ui.setupUi(LoginPage)
    LoginPage.show()

    sys.exit(app.exec_())
