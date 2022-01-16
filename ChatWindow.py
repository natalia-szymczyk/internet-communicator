from PyQt5 import QtCore
from PyQt5.QtWidgets import QSplitter,QVBoxLayout,QDialog, QPushButton, QApplication, QTextEdit, QLineEdit, QMessageBox, QWidget
import sys

class Ui_ChatWindow(object):
    def setupUi(self, ChatWindow, user):
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

        self.retranslateUi(ChatWindow, user)
        QtCore.QMetaObject.connectSlotsByName(ChatWindow)


    def send(self):
        text = self.message.text()

        if len(text) > 0:
            font = self.chat.font()
            font.setPointSize(13)        
            self.chat.setFont(font)
            self.chat.append("login: " + text)
            self.message.setText("")
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Wrong input")
            msg.setText("Your message is empty.")

            msg.setIcon(QMessageBox.Warning)

            msg.setStandardButtons(QMessageBox.Ok)

            x = msg.exec_()

    
    def retranslateUi(self, ChatWindow, user):
        _translate = QtCore.QCoreApplication.translate
        ChatWindow.setWindowTitle(user + " (jakis opis)")
        
        self.sendButton.setShortcut("Return")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    user = "janek"

    ChatWindow = QWidget()
    ui = Ui_ChatWindow()
    ui.setupUi(ChatWindow, user)
    ChatWindow.show()

    sys.exit(app.exec_())
