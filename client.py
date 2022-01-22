import LoginPage, MainPage, SearchFriend, ChatWindow
# from LoginPage import Ui_LoginPage
# from MainPage import Ui_MainWindow
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import socket

# HOST = "172.27.87.197"
HOST = "127.0.0.1"
PORT = 1100
SIZE = 1024
FORMAT = "utf-8"

def main():

    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.connect((HOST,PORT))
        while True:
            msg=input()
            if msg =="exit":
                break

            s.send(bytes(msg,"utf-8"))

            data = s.recv(1024)
            print(data)

    s.close()

    # LoginPage.main()


if __name__ == '__main__':
    main()



