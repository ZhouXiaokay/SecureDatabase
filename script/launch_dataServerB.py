import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import transmission.tenseal.tenseal_data_pb2_grpc as tenseal_data_pb2_grpc
from databaseServer import DatabaseServer
import grpc
from concurrent import futures


def launch_dataServer():
    max_msg_size = 1000000000
    pk_file = "../transmission/ts_ckks_pk.config"
    options = [('grpc.max_send_message_length', max_msg_size), ('grpc.max_receive_message_length', max_msg_size)]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5), options=options)
    tenseal_data_pb2_grpc.add_DatabaseServerServiceServicer_to_server(DatabaseServer(1, pk_file,"B"), server)
    server.add_insecure_port("127.0.0.1:50053")
    server.start()
    print("grpc server start...")
    server.wait_for_termination()


if __name__ == '__main__':
    launch_dataServer()