import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from keyServer import KeyServer
import transmission.request.request_keyServer_pb2_grpc as request_keyServer_pb2_grpc
import grpc
from concurrent import futures


def launch_keyServer():
    max_msg_size = 1000000000
    sk_ctx_file = "../transmission/ts_ckks.config"
    options = [('grpc.max_send_message_length', max_msg_size), ('grpc.max_receive_message_length', max_msg_size)]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5), options=options)
    request_keyServer_pb2_grpc.add_KeyServerServiceServicer_to_server(KeyServer(sk_ctx_file), server)
    server.add_insecure_port("127.0.0.1:50054")
    server.start()
    print("grpc keyServer start...")
    server.wait_for_termination()

if __name__ == '__main__':
    launch_keyServer()
