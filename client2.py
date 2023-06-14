import socket


with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as client:
    client.connect(("localhost",9999))
    client.send(b"hi hellow client 2")
    print(client.recv(1024).decode())
