# echo-server.py

import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)

    connection, client_addresss = s.accept()

    with connection:
        print(f"Connected by {client_addresss}")
        while True:
            data = connection.recv(1024)

            if data:
                print('*'*80)
                print(data)
