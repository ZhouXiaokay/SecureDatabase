import socket
import threading
import time
import datetime

MAX_BYTES = 1024


def HeartBeatServer(host, port, delay):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_sock.bind((host, port))
    print("Server online!")

    while True:
        time.sleep(delay)
        msg, addr = server_sock.recvfrom(MAX_BYTES)
        # print(addr)
        print(f'{datetime.datetime.now()} >>Receive client message {msg}.')
        server_sock.sendto(("Received.".encode('ascii')), addr)
        print(f'{datetime.datetime.now()} >>Send message back.')


if __name__ == "__main__":
    host = ''
    port = 1236
    delay = 1
    HeartBeatServer(host, port, delay)
