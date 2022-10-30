import sys
import os
import threading
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from keyServer import KeyServer
import transmission.request.request_keyServer_pb2_grpc as request_keyServer_pb2_grpc
import grpc
from transmission.supervise import HeartBeatServer
from concurrent import futures


def launch_keyServer(host, port, delay):
    keyServer_address = host + ":" + str(port)
    max_msg_size = 1000000000
    sk_ctx_file = "../transmission/ts_ckks.config"
    options = [('grpc.max_send_message_length', max_msg_size), ('grpc.max_receive_message_length', max_msg_size)]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5), options=options)
    request_keyServer_pb2_grpc.add_KeyServerServiceServicer_to_server(KeyServer(sk_ctx_file), server)
    server.add_insecure_port(keyServer_address)

    server.start()
    print("grpc keyServer start...")
    # launch heart-beat sever.
    monitor_server = threading.Thread(target=HeartBeatServer, args=(host, port, delay))
    monitor_server.setDaemon(True)
    monitor_server.start()
    # print(threading.enumerate())
    print("monitor keyserver service start... ")

    server.wait_for_termination()

if __name__ == '__main__':
    host = "10.254.19.25"
    port = 50054
    delay = 2
    launch_keyServer(host, port, delay)
