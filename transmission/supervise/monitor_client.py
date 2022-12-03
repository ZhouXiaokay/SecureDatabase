import socket
import threading
import time
import datetime

MAX_BYTES = 1024


# UDP Version
def heart_beat_client(host, port, delay):
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    is_server_alive_count = 0

    def recv():
        nonlocal is_server_alive_count
        while True:
            try:
                msg, addr = client_sock.recvfrom(MAX_BYTES)
            except Exception as e:
                print(f'{host}:{port}. {e}')
                continue
            if (addr == (host, port)) and len(msg) != 0:
                is_server_alive_count += 1
            if is_server_alive_count > 10000:
                is_server_alive_count = 0

    recv_thread = threading.Thread(target=recv)
    recv_thread.setDaemon(True)
    recv_thread.start()
    IS_SERVER_ALIVE = True

    while True:
        try:
            client_sock.sendto(f'\"{host}:{port}\"'.encode('ascii'), (host, port))
        except Exception as e:
            print(f'{host}:{port}. {e}')
            IS_SERVER_ALIVE = False

        if IS_SERVER_ALIVE:
            count_status = is_server_alive_count
            time.sleep(delay)
            if count_status != is_server_alive_count:
                print(f'{datetime.datetime.now()} >>{host}:{port} Server online!')
                continue

        print(f'{datetime.datetime.now()} >>{host}:{port} Server offline!')
        IS_SERVER_ALIVE = True
