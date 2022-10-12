from requestServer.parsing import *


class RequestServer(request_data_pb2_grpc.RequestTransmissionServicer):

    def __init__(self, address, pk_ctx_file):
        self.address = address
        self.sleep_time = 0.1
        pk_bytes = open(pk_ctx_file, "rb").read()
        self.pk_ctx = ts.context_from(pk_bytes)

    def RequestParsing(self, request, context):

        enc_vector = requestParsing(request,self.pk_ctx)
        results = resultsDecrypt(enc_vector)
        response = request_data_pb2.results(msg=results)

        return response
