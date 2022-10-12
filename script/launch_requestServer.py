from concurrent import futures
from requestServer import RequestServer
import grpc

import transmission.request.request_data_pb2_grpc as request_data_pb2_grpc


def launch_requestServer():
    max_msg_size = 1000000000
    sk_ctx_file = "../transmission/ts_ckks.config"
    options = [('grpc.max_send_message_length', max_msg_size), ('grpc.max_receive_message_length', max_msg_size)]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5), options=options)
    request_data_pb2_grpc.add_RequestTransmissionServicer_to_server(RequestServer(1,sk_ctx_file),server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("grpc server start...")
    server.wait_for_termination()

if __name__ == '__main__':
    launch_requestServer()