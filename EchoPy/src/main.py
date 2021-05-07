import socket
from time import sleep

HOST = '127.0.0.1'
PORT = 8881

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print("Bound and listening...")
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        sleep(3)
        while True:
            print("Sending data...")
            conn.sendall("Ping!".encode('utf-8'))
            sleep(1)
            data = conn.recv(5)
            print("Received: ", end='')
            print(data.decode('utf-8'))
            sleep(1)