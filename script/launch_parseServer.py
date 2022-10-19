from parseServer import ParseServer
from concurrent import futures
import grpc

import transmission.request.request_parseServer_pb2_grpc as request_parseServer_pb2_grpc


def launch_parseServer():
    address_dict = {"DATABASE_A": "127.0.0.1:50052", "KEYSERVER": "127.0.0.1:50054","DATABASE_B": "127.0.0.1:50053"}
    max_msg_size = 1000000000
    pk_ctx_file = "../transmission/ts_ckks_pk.config"
    options = [('grpc.max_send_message_length', max_msg_size), ('grpc.max_receive_message_length', max_msg_size)]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5), options=options)
    request_parseServer_pb2_grpc.add_ParseServerServiceServicer_to_server(ParseServer(address_dict, pk_ctx_file), server)
    server.add_insecure_port("127.0.0.1:50051")
    server.start()
    print("grpc server start...")
    server.wait_for_termination()


if __name__ == '__main__':
    launch_parseServer()
