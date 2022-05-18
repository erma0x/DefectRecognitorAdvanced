import socket


MESSAGE = b'hello world'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 65432))
s.send(MESSAGE)
