from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from User import User, getUser, addFriend
from PyQt5.QtWidgets import QMessageBox, QSplitter,QVBoxLayout, QPushButton, QTextEdit, QLineEdit, QMessageBox
from threading import Thread 
import socket
import sys
from datetime import datetime
import os.path


app = QtWidgets.QApplication(sys.argv)
LoginPage = QtWidgets.QMainWindow()

client_socket = None
active = True
chat_opened = False
currentLogin = ""
currentFriend = ""

class ClientThread(Thread):
    def __init__(self,window): 
        Thread.__init__(self) 
        self.window = window

    def run(self): 
        host = "172.27.91.201"
        port = 8858
        BUFFER_SIZE = 2000 
        global client_socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

        client_socket.connect((host, port))
       
        while active:   
            data = client_socket.recv(BUFFER_SIZE).decode("unicode_escape")
            msg = data.split("++")
            msg = msg[1:-1]

            if len(msg) > 0 and len(msg[0]) > 1:

                friend = msg[0].split(":")
                friend = friend[0]

                print(f"msg: {msg}, friend: {friend}")

                if friend == currentFriend:
                    global ui
                    ui.chat.append(msg[0])       
                     

        client_socket.shutdown(socket.SHUT_RDWR) 
        client_socket.close()
        sys.exit()


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
        self.errorLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.errorLabel.setObjectName("errorLabel")

        LoginPage.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(LoginPage)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 342, 26))
        self.menubar.setObjectName("menubar")
        LoginPage.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(LoginPage)
        self.statusbar.setObjectName("statusbar")
        LoginPage.setStatusBar(self.statusbar)

        self.getAllUsers()

        self.retranslateUi(LoginPage)
        QtCore.QMetaObject.connectSlotsByName(LoginPage)

        self.signInButton.clicked.connect(self.signInCheck)

        self.signUpButton.clicked.connect(self.signUpCheck)


    def getAllUsers(self):
        
        self.users = []
        self.login_password = []

        with open(r"users.txt", "r") as f:
            for line in f:
                tmp = line.split()
                login, password, name = tmp[0], tmp[1], " ".join(tmp[2:])
                self.users.append([login, password, name])
                self.login_password.append([login, password])

        self.logins = [login for [login, _, _] in self.users]


    def loginCheck(self, login):
        if len(login) < 5:
            self.errorLabel.setText("Login too short")
            return False
        elif len(login) > 20:
            self.errorLabel.setText("Login too long.")
            return False

        available = True
        
        if login in self.logins:
            available = False

        if available == False:
            self.errorLabel.setText("Login not available.")
            return False

        return True


    def passwordCheck(self, password):
        if len(password) < 5:
            self.errorLabel.setText("Password too short")
            return False
        elif len(password) > 20:
            self.errorLabel.setText("Password too long.")
            return False
        
        return True


    def signUpCheck(self):
        name = self.nameInputUp.text()
        login = self.loginInputUp.text()
        password = self.passwordInputUp.text()
        
        if self.passwordCheck(password) and self.loginCheck(login):
            self.signUp(name, login, password)


    def signUp(self, name, login, password):
        s1 = f"\n{login} {password} {name}"
        file = open(r"users.txt", 'a')
        file.write(s1)
        file.close()

        s2 = f"\n{login} "
        file = open(r"friends.txt", 'a')
        file.write(s2)
        file.close()

        user = User(login, password)
        
        self.signIn(user)


    def openMainPage(self, user):
        self.window = QtWidgets.QMainWindow()   
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window, user)
        self.window.show()
        LoginPage.hide()
        

    def signInCheck(self):
        login = self.loginInputIn.text()
        password = self.passwordInputIn.text()

        if [login, password] in self.login_password:
            correctData = True 
        else:
            correctData = False    

        if correctData:
            user = User(login, password)
            self.signIn(user)
        else:
            self.errorLabel.setText("Wrong data.")


    def signIn(self, user):
        client_socket.send(bytes(f"++LOGIN++{user.login}++","utf-8"))
        global currentLogin
        currentLogin = user.login
        self.openMainPage(user)


    def retranslateUi(self, LoginPage):
        _translate = QtCore.QCoreApplication.translate
        LoginPage.setWindowTitle(_translate("LoginPage", "Gadu Gadu"))
        self.label1.setText("Need an account?")
        self.loginInputUp.setPlaceholderText("Login")
        self.passwordInputUp.setPlaceholderText("Password")
        self.signUpButton.setText("Sign up")
        self.label2.setText("Already a user?")
        self.loginInputIn.setPlaceholderText("Login")
        self.passwordInputIn.setPlaceholderText("Password")
        self.nameInputUp.setPlaceholderText("Name")
        self.signInButton.setText("Sign in")
        self.signInButton.setShortcut("Return")


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, user):
        self.currentUser = user
        global client_socket
        # client_socket.send(bytes(f"MAIN+{self.currentUser.login}","utf-8"))
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

        self.refreshButton = QtWidgets.QPushButton(self.centralwidget)
        self.refreshButton.setGeometry(QtCore.QRect(10, 510, 93, 28))
        self.refreshButton.setFont(font)

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

        # self.chatWindows = []
        oldFriends = len(self.currentUser.friends)

        self.listWidget.itemDoubleClicked.connect(self.openChat)

        self.addFriendButton.clicked.connect(self.addFriend)

        self.logOutButton.clicked.connect(self.askBeforeLogOut)

        self.descriptionButton.clicked.connect(self.changeDescription)

        self.refreshButton.clicked.connect(lambda: self.updateFriendsList(oldFriends))


    def changeDescription(self):
        description = self.descriptionEdit.text()
        self.currentUser.updateDescription(description)


    def openChat(self, element):
        start = '('
        end = ')'
        friendsString = element.text()
        friendLogin = friendsString[friendsString.find(start)+len(start):friendsString.rfind(end)]
        friend = getUser(friendLogin)
        global client_socket
        client_socket.send(bytes(f"++CHAT++{self.currentUser.login}++{friendLogin}++","utf-8"))
        self.openChatWindow(friend)
        

    def openChatWindow(self, friend):
        global chat_opened
        chat_opened = True
        global currentFriend
        currentFriend = friend.login
        self.chat_window = QtWidgets.QWidget()  
        global ui      
        ui.setupUi(self.chat_window, self.currentUser, friend)
        self.chat_window.show()
        # self.chatWindows.append(self.chat_window)


    def addFriend(self):
        self.openSearchFriend()


    def openSearchFriend(self):
        self.window = QtWidgets.QMainWindow()   
        self.ui = Ui_SearchFriend()
        self.ui.setupUi(self.window, self.currentUser)
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
            self.logOut()


    def logOut(self):
        client_socket.send(bytes(f"++LOGOUT++{self.currentUser.login}++","utf-8"))
        # client_socket.close()
        # sys.exit()
        global active
        active = False
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


    def updateFriendsList(self, oldFriends):
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)

        newFriends = len(self.currentUser.friends) - oldFriends

        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        
        for i in range(newFriends):
            item = QtWidgets.QListWidgetItem()
            item.setFont(font)
            self.listWidget.addItem(item)

        for i in range(len(self.currentUser.friends)):
            item = self.listWidget.item(i)
            friend = getUser(self.currentUser.friends[i])
            item.setText(friend.toString())

        self.listWidget.setSortingEnabled(__sortingEnabled)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Gadu Gadu"))
        self.gaduGaduLabel.setText("Gadu Gadu")
        self.yourFriendsLabel.setText("Your friends:")
        self.helloLabel.setText(_translate("MainWindow", f"Hello {self.currentUser.name}! "))
        if len(self.currentUser.description) == 0:
            self.descriptionEdit.setPlaceholderText("My description...")
        else:
            self.descriptionEdit.setText(self.currentUser.description)
        self.addFriendButton.setText("Add a friend")
        self.logOutButton.setText("Log out")
        self.descriptionButton.setText("Change")
        self.refreshButton.setText("Refresh")

        self.updateFriendsList(len(self.currentUser.friends))


class Ui_ChatWindow(object):
    def setupUi(self, ChatWindow, currentUser, friend):
        self.currentUser = currentUser
        self.friend = friend

        logins = [self.currentUser.login, self.friend.login]
        logins.sort()

        self.filename = f"{logins[0]}_{logins[1]}.txt"

        ChatWindow.setObjectName("ChatWindow")
        ChatWindow.resize(500, 500)

        self.message = QLineEdit(ChatWindow)
        self.message.resize(480,100)
        self.message.move(10,350)

        self.sendButton = QPushButton("Send", ChatWindow)
        self.sendButton.resize(480,30)
        self.font = self.sendButton.font()
        self.font.setPointSize(15)
        self.sendButton.setFont(self.font)
        self.sendButton.move(10,460)
        self.sendButton.clicked.connect(self.send)

        self.chatBody = QVBoxLayout(ChatWindow)
        splitter = QSplitter(QtCore.Qt.Vertical)

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)

        splitter.addWidget(self.chat)
        splitter.addWidget(self.message)
        splitter.setSizes([400,100])

        splitter2 = QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter)
        splitter2.addWidget(self.sendButton)
        splitter2.setSizes([200,10])

        self.chatBody.addWidget(splitter2)

        self.retranslateUi(ChatWindow)
        QtCore.QMetaObject.connectSlotsByName(ChatWindow)

        self.dateWritten = False
        self.readFromFile()


    def readFromFile(self):
        font = self.chat.font()
        font.setPointSize(13)        
        self.chat.setFont(font)

        if os.path.isfile(self.filename):        
            with open(self.filename, "rb") as f:
                lines = f.readlines()
                for line in lines:
                    self.chat.append(line.decode("utf-8"))
        else:
            f = open(self.filename, "w+")


    def writeDate(self):
        with open(self.filename, 'a+') as f:
                f.write('\n')
                f.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                f.write('\n')
        
        font = self.chat.font()
        font.setPointSize(13)        
        self.chat.setFont(font)
        self.chat.append(f"\n{datetime.today().strftime('%Y-%m-%d %H:%M:%S')}\n")

        self.dateWritten = True

                      
    def send(self):
        text = self.message.text()

        if not self.dateWritten:
            self.writeDate()

        if len(text) > 0:
            font = self.chat.font()
            font.setPointSize(13)        
            self.chat.setFont(font)
            self.chat.append(f"{self.currentUser.login}: {text}")
            self.message.setText("")
            
            client_socket.send(bytes(f"++MSG++{self.currentUser.login}++{self.friend.login}++{text}++","utf-8"))
            

            with open(self.filename, 'a+') as f:
                f.write(f"{self.currentUser.login}: {text} \n")
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Wrong input")
            msg.setText("Your message is empty.")

            msg.setIcon(QMessageBox.Warning)

            msg.setStandardButtons(QMessageBox.Ok)

            x = msg.exec_()

    
    def retranslateUi(self, ChatWindow):
        _translate = QtCore.QCoreApplication.translate
        ChatWindow.setWindowTitle(self.friend.toString())
        
        self.sendButton.setShortcut("Return")


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
            if foundFriend.login in self.currentUser.friends:
                self.errorLabel.setText("Already Your friend")
            elif foundFriend.login == self.currentUser.login:
                self.errorLabel.setText("This is your login")
            else:
                addFriend(self.currentUser, foundFriend)
                client_socket.send(bytes(f"++   ADD++{self.currentUser.login}++{foundFriend.login}++", "utf-8"))
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
        self.friendsLogin.setPlaceholderText("Login")
        self.label.setText("Search a friend:")

        self.searchButton.setShortcut("Return")


ui = Ui_ChatWindow()

def main():
    ui = Ui_LoginPage()
    ui.setupUi(LoginPage)
    
    clientThread=ClientThread(LoginPage)
    clientThread.daemon = True
    clientThread.start()
    
    LoginPage.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
