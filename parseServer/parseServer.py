from parseServer.parsing import *
import transmission.request.request_parseServer_pb2 as request_parseServer_pb2
import transmission.request.request_parseServer_pb2_grpc as request_parseServer_pb2_grpc


class ParseServer(request_parseServer_pb2_grpc.ParseServerServiceServicer):

    def __init__(self, address_dict, pk_ctx_file):
        self.address_dict = address_dict
        self.sleep_time = 0.1
        pk_bytes = open(pk_ctx_file, "rb").read()
        self.pk_ctx = ts.context_from(pk_bytes)

        self.max_msg_size = 1000000000
        self.options = [('grpc.max_send_message_length', self.max_msg_size),
                        ('grpc.max_receive_message_length', self.max_msg_size)]

    def RequestParsing(self, request, context):
        enc_vector = request_parsing(request, self.pk_ctx, self.address_dict, self.options)

        keyserver_stub = get_keyserver_stub(self.address_dict, self.options)
        return_results(keyserver_stub, enc_vector, request)

        response = request_parseServer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response
