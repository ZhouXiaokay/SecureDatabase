import sys
import os
import threading
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from key_server import KeyServer
import transmission.tenseal.tenseal_key_server_pb2_grpc as tenseal_key_server_pb2_grpc
import grpc
from transmission.supervise import HeartBeatServer
from concurrent import futures


def launch_key_server(host, port, delay):
    keyServer_address = host + ":" + str(port)
    max_msg_size = 1000000000
    sk_ctx_file = "../transmission/ts_ckks.config"
    options = [('grpc.max_send_message_length', max_msg_size), ('grpc.max_receive_message_length', max_msg_size)]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5), options=options)
    tenseal_key_server_pb2_grpc.add_KeyServerServiceServicer_to_server(KeyServer(sk_ctx_file), server)
    server.add_insecure_port(keyServer_address)

    server.start()
    print("grpc key_server start...")
    # launch heart-beat sever.
    monitor_server = threading.Thread(target=HeartBeatServer, args=(host, port, delay))
    monitor_server.setDaemon(True)
    monitor_server.start()
    # print(threading.enumerate())
    print("monitor keyserver service start... ")

    server.wait_for_termination()

if __name__ == '__main__':
    host = "127.0.0.1"
    port = 50054
    delay = 2
    launch_key_server(host, port, delay)
