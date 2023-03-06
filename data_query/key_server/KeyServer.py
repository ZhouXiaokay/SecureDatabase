import transmission.tenseal.tenseal_key_server_pb2 as tenseal_key_server_pb2
import transmission.tenseal.tenseal_key_server_pb2_grpc as tenseal_key_server_pb2_grpc
import transmission.tenseal.tenseal_client_proxy_pb2 as tenseal_client_proxy_pb2
import transmission.tenseal.tenseal_client_proxy_pb2_grpc as tenseal_client_proxy_pb2_grpc
import grpc
import tenseal as ts
import pickle
from .utils import *
import numpy as np

class KeyServer(tenseal_key_server_pb2_grpc.KeyServerServiceServicer):

    def __init__(self, sk_ctx_file):
        self.db_num = 3
        sk_ctx_bytes = open(sk_ctx_file, "rb").read()
        self.sk_ctx = ts.context_from(sk_ctx_bytes)
        self.max_msg_size = 1000000000
        self.options = [('grpc.max_send_message_length', self.max_msg_size),
                        ('grpc.max_receive_message_length', self.max_msg_size)]
        self.total_noise_list = []
        self.sleep_time = 0.1
        self.n_sum_request = 0
        self.n_sum_response = 0

    def reset_sum(self):
        self.n_sum_request = 0
        self.n_sum_response = 0

    def return_enc_query_result(self, request, context):
        # remove the noise list by cid and qid
        remove_noise_list(request.cid, request.qid, self.total_noise_list)

        # receive and decrypt the results from parse_server
        ip_address = request.ip_address
        enc_serialize_msg = request.enc_result
        enc_vector = ts.ckks_vector_from(self.sk_ctx, enc_serialize_msg)
        dec_vector = enc_vector.decrypt()

        # make request and send it to client_proxy
        dec_serialize_msg = pickle.dumps(dec_vector)
        result_request = tenseal_client_proxy_pb2.query_result_key_server(cid=request.cid, qid=request.qid,
                                                                          dec_result=dec_serialize_msg)

        channel = grpc.insecure_channel(ip_address, options=self.options)
        stub = tenseal_client_proxy_pb2_grpc.ClientProxyServiceStub(channel)
        stub.return_dec_query_result(result_request)

        response = tenseal_key_server_pb2.google_dot_protobuf_dot_empty__pb2.Empty()

        return response

    def boolean_positive(self, request, context):
        enc_serialize_msg = request.vector_msg
        enc_vector = ts.ckks_vector_from(self.sk_ctx, enc_serialize_msg)
        dec_vector = enc_vector.decrypt()
        flag = False
        if dec_vector[0] > 0:
            flag = True

        response = tenseal_key_server_pb2.boolean_result(bool_msg=flag)

        return response



    def generate_noise(self, request, context):
        qid = request.qid
        cid = request.cid
        noise_type = request.type
        noise_list = generate_noise_list(self.db_num, noise_type)
        noise_dict = {'cid': cid, 'qid': qid, 'noise_list': noise_list}
        self.total_noise_list.append(noise_dict)
        response = tenseal_key_server_pb2.google_dot_protobuf_dot_empty__pb2.Empty()

        return response

    def get_noise(self, request, context):
        noise = get_noise(request.cid, request.qid, request.db_name, self.total_noise_list)
        noise_serialized_msg = pickle.dumps(noise)

        response = tenseal_key_server_pb2.responseNoise(noiseMsg=noise_serialized_msg)

        return response

    def sqrt_enc_vector(self, request, context):
        enc_serialize_msg = request.vector_msg
        enc_vector = ts.ckks_vector_from(self.sk_ctx, enc_serialize_msg)
        dec_vector = enc_vector.decrypt()
        sqrt_dec_vector = np.sqrt(dec_vector)

        sqrt_plain_vector = ts.plain_tensor(sqrt_dec_vector)
        sqrt_enc_vector = ts.ckks_vector(self.sk_ctx, sqrt_plain_vector)
        sqrt_serialized_msg = sqrt_enc_vector.serialize()
        response = tenseal_key_server_pb2.vector(vector_msg=sqrt_serialized_msg)

        return response

    def div_enc_vector(self, request, context):
        # get the dividend vector
        dividend_enc_msg = request.dividend_msg
        dividend_enc_vector = ts.ckks_vector_from(self.sk_ctx, dividend_enc_msg)
        dividend_dec_vector = dividend_enc_vector.decrypt()
        # get the divisor vector
        divisor_enc_msg = request.divisor_msg
        divisor_enc_vector = ts.ckks_vector_from(self.sk_ctx, divisor_enc_msg)
        divisor_dec_vector = divisor_enc_vector.decrypt()
        # get the division(dividend/divisor)
        div_dec_vector = np.divide(dividend_dec_vector, divisor_dec_vector)

        # make response and return
        div_plain_vector = ts.plain_tensor(div_dec_vector)
        div_enc_vector = ts.ckks_vector(self.sk_ctx, div_plain_vector)
        sqrt_serialized_msg = div_enc_vector.serialize()
        response = tenseal_key_server_pb2.vector(vector_msg=sqrt_serialized_msg)

        return response

    def unpack_enc_vector(self, request, context):
        enc_serialize_msg = request.vector_msg
        import pickle
        enc_vector = pickle.loads(enc_serialize_msg)
        unpacked_enc_vector = []
        for i in range(len(enc_vector)):
            unpacked_enc_vector.append(ts.ckks_vector_from(self.sk_ctx, enc_vector[i]).decrypt()[0])
        plain_vector = ts.plain_tensor(unpacked_enc_vector)
        enc_vector = ts.ckks_vector(self.sk_ctx, plain_vector)
        sqrt_serialized_msg = enc_vector.serialize()
        response = tenseal_key_server_pb2.vector(vector_msg=sqrt_serialized_msg)
        return response

    def boolean_positive_proxi(self, request, context):
        enc_serialize_msg = request.vector_msg
        enc_vector = ts.ckks_vector_from(self.sk_ctx, enc_serialize_msg)
        dec_vector = enc_vector.decrypt()
        flag = False
        if dec_vector[0] >= 0 or abs(dec_vector[0]) <= 1e-8: # close to zero
            flag = True

        response = tenseal_key_server_pb2.boolean_result(bool_msg=flag)

        return response

    def boolean_equal_proxi(self, request, context):
        enc_serialize_msg = request.vector_msg
        enc_vector = ts.ckks_vector_from(self.sk_ctx, enc_serialize_msg)
        dec_vector = enc_vector.decrypt()
        flag = False
        print(dec_vector[0])
        if abs(dec_vector[0]) <= 1e-8:
            flag = True

        response = tenseal_key_server_pb2.boolean_result(bool_msg=flag)

        return response