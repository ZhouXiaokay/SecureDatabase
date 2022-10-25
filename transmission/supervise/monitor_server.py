import socket
import time

MAX_BYTES = 1024

def HeartBeatServer(host, port, delay):

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_sock.bind((host, port))
    print("Server online!")

    while True:
        time.sleep(delay)
        msg, addr = server_sock.recvfrom(MAX_BYTES)
        print(f'Receive client message {msg}.')
        server_sock.connect(addr)
        server_sock.send("Received.".encode('ascii'))
        print(f'Send message back.')

if __name__ =="__main__":
    host = ''
    port = 1236
    delay = 2
    HeartBeatServer(host, port, delay)