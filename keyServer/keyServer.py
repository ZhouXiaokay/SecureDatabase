import transmission.request.request_data_pb2 as request_data_pb2
import transmission.request.request_data_pb2_grpc as request_data_pb2_grpc
import grpc
import tenseal as ts
import pickle

class KeyServer(request_data_pb2_grpc.RequestTransmissionServicer):

    def __init__(self, sk_ctx_file):
        sk_ctx_bytes = open(sk_ctx_file, "rb").read()
        self.sk_ctx = ts.context_from(sk_ctx_bytes)

    def RequestDecrypt(self, request, context):
        # receive and decrypt the results from requestServer
        msg = request.msg
        enc_vector = ts.ckks_vector_from(self.sk_ctx, msg)
        dec_vector = enc_vector.decrypt()

        # make responses and send it to requestServer
        serialize_msg = pickle.dumps(dec_vector)
        response = request_data_pb2.results(msg=serialize_msg)

        return response
