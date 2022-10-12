import transmission.teanseal.tenseal_data_pb2_grpc as tenseal_data_pb2_grpc
from databaseServer import DatabaseServer
import grpc
from concurrent import futures


def launch_server():
    max_msg_size = 1000000000
    pk_file = "../transmission/ts_ckks_pk.config"
    options = [('grpc.max_send_message_length', max_msg_size), ('grpc.max_receive_message_length', max_msg_size)]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5), options=options)
    tenseal_data_pb2_grpc.add_SafeTransmissionServicer_to_server(DatabaseServer(1, pk_file,"A"), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("grpc server start...")
    server.wait_for_termination()


if __name__ == '__main__':
    launch_server()