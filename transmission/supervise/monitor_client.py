import socket
import threading
import time
import datetime

MAX_BYTES = 1024


def HeartBeatClient(host, port, delay):
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    is_server_alive_count = 0

    def recv():
        nonlocal is_server_alive_count
        while True:
            try:
                msg, addr = client_sock.recvfrom(MAX_BYTES)
            except:
                continue
            is_server_alive_count += 1
            if is_server_alive_count > 10000:
                is_server_alive_count = 0

    recv_thread = threading.Thread(target=recv)
    recv_thread.setDaemon(True)
    recv_thread.start()
    IS_SERVER_ALIVE = True
    # print(threading.enumerate())

    while True:
        client_sock.connect((host, port))
        try:
            client_sock.send('Connect.'.encode('ascii'))
        except:
            IS_SERVER_ALIVE = False

        if IS_SERVER_ALIVE:
            count_status = is_server_alive_count
            time.sleep(delay)
            if count_status != is_server_alive_count:
                print(f'{datetime.datetime.now()} >>{host}:{port} Server  online!')
                continue

        print(f'{datetime.datetime.now()} >>{host}:{port} Server offline!')
        IS_SERVER_ALIVE = True


if __name__ == "__main__":
    host = ''
    port = 1236
    delay = 5
    HeartBeatClient(host, port, delay)
