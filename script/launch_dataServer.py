import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import transmission.tenseal.tenseal_data_pb2_grpc as tenseal_data_pb2_grpc
from databaseServer import DatabaseServer
import grpc
import threading
from transmission.supervise import HeartBeatServer
from concurrent import futures


def launch_dataServer(host, port, delay):
    dataServer_address = host + ":" + str(port)
    max_msg_size = 1000000000
    pk_file = "../transmission/ts_ckks_pk.config"
    options = [('grpc.max_send_message_length', max_msg_size), ('grpc.max_receive_message_length', max_msg_size)]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5), options=options)
    tenseal_data_pb2_grpc.add_DatabaseServerServiceServicer_to_server(DatabaseServer(dataServer_address, pk_file, 1),
                                                                      server)
    server.add_insecure_port(dataServer_address)
    server.start()
    print("grpc dataServer_1 start...")

    #launch heart-beat sever.
    monitor_server = threading.Thread(target=HeartBeatServer, args=(host, port, delay))
    monitor_server.setDaemon(True)
    monitor_server.start()
    # print(threading.enumerate())
    print("monitor server_1 service start... ")
    server.wait_for_termination()


if __name__ == '__main__':
    host = "10.254.19.25"
    port = 50052
    delay = 2
    launch_dataServer(host, port, delay)
