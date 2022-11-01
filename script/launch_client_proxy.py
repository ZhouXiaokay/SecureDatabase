import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from client_proxy import ClientProxy
from concurrent import futures
import grpc

import transmission.tenseal.tenseal_client_proxy_pb2_grpc as tenseal_client_proxy_pb2_grpc


def launch_client_proxy():

    max_msg_size = 1000000000
    options = [('grpc.max_send_message_length', max_msg_size), ('grpc.max_receive_message_length', max_msg_size)]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5), options=options)
    tenseal_client_proxy_pb2_grpc.add_ClientProxyServiceServicer_to_server(
        ClientProxy('127.0.0.1:50051', '127.0.0.1:50060'), server)
    server.add_insecure_port('127.0.0.1:50060')
    server.start()
    print("grpc client_proxy start...")
    server.wait_for_termination()


if __name__ == '__main__':
    launch_client_proxy()
