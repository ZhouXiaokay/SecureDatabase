import transmission.request.request_data_pb2 as request_data_pb2
import transmission.request.request_data_pb2_grpc as request_data_pb2_grpc
import time

class RequestServer(request_data_pb2_grpc.RequestTransmissionServicer):

    def __init__(self,address):
        self.address = address
        self.sleep_time = 0.1