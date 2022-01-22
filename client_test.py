import select 
import socket
import sys
import msvcrt

HOST = "127.0.0.1"
PORT = 1100

tcpClientA=None

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    # s.connect((HOST,PORT))

    print("dziala python")

    try :
        s.connect((HOST,PORT))
    except :
        print("Unable to connect")
        sys.exit()

    while True:
        print("petla")
        # socket_list = [socket.socket(), s]

        # read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

        read_sockets = select.select([s], [], [], 1)[0]
   
        if msvcrt.kbhit(): 
            read_sockets.append(sys.stdin)

        for sock in read_sockets:            
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(4096)
                if not data :
                    print('\nDisconnected from chat server')
                    sys.exit()
                else :
                    #print data
                    data = s.recv(1024)
                    print("\n >> ", data.decode(), "\n") 

            else :
                opt = input("opcja")

                if opt == "1":
                    login = input("login: ")
                    password = input("password: ")
                    s.send(bytes(f"LOGIN|{login}|{password}", "utf-8"))
                elif opt == 2:
                    login = input("login: ")
                    s.send(bytes("LOGOUT|{login}", "utf-8"))
                elif opt == "0":
                    break
                else:
                    s.send(bytes("nic konkretnego", "utf-8"))



