from PyQt5 import QtCore
from PyQt5.QtWidgets import QSplitter,QVBoxLayout,QDialog, QPushButton, QApplication, QTextEdit, QLineEdit, QMessageBox
import sys


class Window(QDialog):
    def __init__(self, user):
        super().__init__()

        self.message = QLineEdit(self)
        self.message.resize(480,100)
        self.message.move(10,350)

        self.send_button = QPushButton("Send", self)
        self.send_button.resize(480,30)
        self.button_font = self.send_button.font()
        self.button_font.setPointSize(15)
        self.send_button.setFont(self.button_font)
        self.send_button.move(10,460)
        self.send_button.clicked.connect(self.send)

        self.chat_body = QVBoxLayout(self)
        splitter = QSplitter(QtCore.Qt.Vertical)

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)

        splitter.addWidget(self.chat)
        splitter.addWidget(self.message)
        splitter.setSizes([400,100])

        splitter2 = QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter)
        splitter2.addWidget(self.send_button)
        splitter2.setSizes([200,10])

        self.chat_body.addWidget(splitter2)

        self.setWindowTitle(user + " (jakis opis)")
        self.resize(500, 500)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    user = "login"
    window = Window(user)
    window.exec()
    sys.exit(app.exec_())
