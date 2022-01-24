from PyQt5 import QtCore
from PyQt5.QtWidgets import QSplitter,QVBoxLayout,QDialog, QPushButton, QApplication, QTextEdit, QLineEdit, QMessageBox, QWidget
import sys
from datetime import datetime

from User import getUser


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

        self.readFromFile()
        self.dateWritten = False

    def readFromFile(self):
        font = self.chat.font()
        font.setPointSize(13)        
        self.chat.setFont(font)
        
        with open(self.filename, "r") as f:
            lines = f.readlines()
            for line in lines:
                self.chat.append(line)


    def writeDate(self):
        with open(self.filename, 'a+') as f:
                f.write('\n')
                f.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                f.write('\n')

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


app = QApplication(sys.argv)
ChatWindow = QWidget()
ui = Ui_ChatWindow()

if __name__ == '__main__':
    user1 = getUser("basia")
    user2 = getUser("jasia")

    # ChatWindow = QWidget()
    # ui = Ui_ChatWindow()
    ui.setupUi(ChatWindow, user1, user2)
    ChatWindow.show()

    ui.chat.append("proba: proba")

    sys.exit(app.exec_())
