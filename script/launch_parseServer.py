import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from parseServer import ParseServer
from concurrent import futures
import grpc
import threading
from transmission.supervise import HeartBeatClient
import transmission.request.request_parseServer_pb2_grpc as request_parseServer_pb2_grpc


def launch_parseServer(host, port, delay):
    parseServer_address = host + ":" + str(port)
    address_dict = {"DATABASE_1": "127.0.0.1:50052", "KEYSERVER": "127.0.0.1:50054", "DATABASE_2": "127.0.0.1:50053",
                    "DATABASE_3": "127.0.0.1:50055"}
    max_msg_size = 1000000000
    pk_ctx_file = "../transmission/ts_ckks_pk.config"
    options = [('grpc.max_send_message_length', max_msg_size), ('grpc.max_receive_message_length', max_msg_size)]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5), options=options)
    request_parseServer_pb2_grpc.add_ParseServerServiceServicer_to_server(ParseServer(address_dict, pk_ctx_file),
                                                                          server)
    server.add_insecure_port(parseServer_address)
    server.start()
    print("grpc parseServer start...")

    #launch heart-beat client
    for index, value in enumerate(address_dict.values()):
        server_host, server_port = value.split(':')
        monitor_client = threading.Thread(target=HeartBeatClient, args=(server_host, int(server_port), delay))
        monitor_client.setDaemon(True)
        monitor_client.start()
        print(f"monitor client {index+1} service start... ")

    server.wait_for_termination()


if __name__ == '__main__':
    host = "127.0.0.1"
    port = 50051
    delay = 5
    launch_parseServer(host, port, delay)
