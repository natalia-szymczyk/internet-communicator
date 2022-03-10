# Internet communicator

### General info
This is an application that allows communication between users using concurrent approach and TCP server. 

### Technologies
The client has been implemented in Python using the library PyQt5 to work with GUI. <br>
The server has been written in C.

### Setup
The server can be run on a terminal with Linux kernel (e.g. WSL, WSL2) with the command:

`gcc -g -Wall -pthread serverTCPmultithread.c - lpthread -o server && ./server`

The client can be run on system with properly configured PyQt5 package with command:

`python client.py`


### Description

The user can register when using the application for the first time, or log in with his data, if he already has an account. 

<p align="center">
  <img src="https://github.com/natalia-szymczyk/internet-communicator/blob/main/windows/login_page.jpg" />
</p>

The basic functionality for logged in users is sending and receiving messages with users who are friends. It is possible to search and add friends based on their login. User can also set / change his description, which is visible to his friends.

<p align="center">
  <img src="https://github.com/natalia-szymczyk/internet-communicator/blob/main/windows/main_page.jpg" />
</p>
