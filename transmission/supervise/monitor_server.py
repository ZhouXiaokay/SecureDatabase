import socket
import time
import datetime

MAX_BYTES = 1024


# UDP Version
def heart_beat_server(host, port, delay):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_sock.bind((host, port))
    print(f"Server {host}:{port} online!")

    while True:
        # time.sleep(delay)
        msg, addr = server_sock.recvfrom(MAX_BYTES)
        print(f'{datetime.datetime.now()} >>Receive client message: {msg.decode("ascii")}.')
        server_sock.sendto(("Connection confirmed.".encode('ascii')), addr)
        print(f'{datetime.datetime.now()} >>Send message back.')
