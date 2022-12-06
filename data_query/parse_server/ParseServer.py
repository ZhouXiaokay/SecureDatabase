import transmission.tenseal.tenseal_parse_server_pb2 as tenseal_parse_server_pb2
import transmission.tenseal.tenseal_parse_server_pb2_grpc as tenseal_parse_server_pb2_grpc
from .utils import *
from .parsing import *


class ParseServer(tenseal_parse_server_pb2_grpc.ParseServerServiceServicer):

    def __init__(self, address_dict, pk_ctx_file):
        self.address_dict = address_dict
        self.sleep_time = 0.1
        pk_bytes = open(pk_ctx_file, "rb").read()
        self.pk_ctx = ts.context_from(pk_bytes)

        self.max_msg_size = 1000000000
        self.options = [('grpc.max_send_message_length', self.max_msg_size),
                        ('grpc.max_receive_message_length', self.max_msg_size)]

    def parse_request(self, request, context):
        enc_vector = request_parsing(request, self.pk_ctx, self.address_dict, self.options)

        key_server_stub = get_key_server_stub(self.address_dict, self.options)
        return_results(key_server_stub, enc_vector, request)

        response = tenseal_parse_server_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response

