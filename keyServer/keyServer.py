import transmission.request.request_keyServer_pb2 as request_keyServer_pb2
import transmission.request.request_keyServer_pb2_grpc as request_keyServer_pb2_grpc
import transmission.request.request_clientProxy_pb2 as request_clientProxy_pb2
import transmission.request.request_clientProxy_pb2_grpc as request_clientProxy_pb2_grpc
import grpc
import tenseal as ts
import pickle
from keyServer.utils import *
import time
import numpy as np


class KeyServer(request_keyServer_pb2_grpc.KeyServerServiceServicer):

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

    def ReturnResult(self, request, context):
        # remove the noise list by cid and qid
        remove_noise_list(request.cid, request.qid, self.total_noise_list)

        # receive and decrypt the results from parseServer
        ipaddress = request.ipaddress
        enc_serialize_msg = request.encResult
        enc_vector = ts.ckks_vector_from(self.sk_ctx, enc_serialize_msg)
        dec_vector = enc_vector.decrypt()

        # make request and send it to clientProxy
        dec_serialize_msg = pickle.dumps(dec_vector)
        result_request = request_clientProxy_pb2.requestDecResult(cid=request.cid, qid=request.qid,
                                                                  decResult=dec_serialize_msg)

        channel = grpc.insecure_channel(ipaddress, options=self.options)
        stub = request_clientProxy_pb2_grpc.ClientProxyServiceStub(channel)
        stub.RequestResult(result_request)

        response = request_keyServer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()

        return response

    def RequestDecrypt(self, request, context):
        # get decrypted vector from encrypted serialized msg;
        enc_serialize_msg = request.vectorMsg
        enc_vector = ts.ckks_vector_from(self.sk_ctx, enc_serialize_msg)
        dec_vector = enc_vector.decrypt()

        # make request and send it to requestServer
        dec_serialize_msg = pickle.dumps(dec_vector)

        response = request_keyServer_pb2.vectorResult(vectorMsg=dec_serialize_msg)

        return response

    def BooleanPositive(self, request, context):
        enc_serialize_msg = request.vectorMsg
        enc_vector = ts.ckks_vector_from(self.sk_ctx, enc_serialize_msg)
        dec_vector = enc_vector.decrypt()
        flag = False
        if dec_vector[0] > 0:
            flag = True

        response = request_keyServer_pb2.booleanResult(boolMsg=flag)

        return response

    def GenerateNoise(self, request, context):
        qid = request.qid
        cid = request.cid
        noise_type = request.type
        noise_list = generate_noise_list(self.db_num, noise_type)
        noise_dict = {'cid': cid, 'qid': qid, 'noise_list': noise_list}
        self.total_noise_list.append(noise_dict)
        response = request_keyServer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()

        return response

    def GetNoise(self, request, context):
        noise = get_noise(request.cid, request.qid, request.db_name, self.total_noise_list)
        noise_serialized_msg = pickle.dumps(noise)

        response = request_keyServer_pb2.responseNoise(noiseMsg=noise_serialized_msg)

        return response

    # def GenerateNoise(self, request, context):
    #
    #     self.n_sum_request += 1
    #     # wait until receiving of all dataServer requests
    #     while self.n_sum_request % self.db_num != 0:
    #         time.sleep(self.sleep_time)
    #
    #     db_name = request.db_name
    #     qid = request.qid
    #     if db_name == 1:
    #         noise_type = request.type
    #         noise_list = generate_noise_list(self.db_num, noise_type)
    #         self.noise_dict[qid] = noise_list
    #
    #     noise = list(self.noise_dict[qid][db_name - 1])
    #     noise_serialized_msg = pickle.dumps(noise)
    #
    #     response = request_keyServer_pb2.responseNoise(noiseMsg=noise_serialized_msg)
    #     self.n_sum_response = self.n_sum_response + 1
    #     while self.n_sum_response % self.db_num != 0:
    #         time.sleep(self.sleep_time)
    #
    #     if db_name == 1:
    #         self.reset_sum()
    #
    #     return response

    def SqrtEncVector(self, request, context):
        enc_serialize_msg = request.vectorMsg
        enc_vector = ts.ckks_vector_from(self.sk_ctx, enc_serialize_msg)
        dec_vector = enc_vector.decrypt()
        sqrt_dec_vector = np.sqrt(dec_vector)

        sqrt_plain_vector = ts.plain_tensor(sqrt_dec_vector)
        sqrt_enc_vector = ts.ckks_vector(self.sk_ctx,sqrt_plain_vector)
        sqrt_serialized_msg = sqrt_enc_vector.serialize()
        response = request_keyServer_pb2.vectorResult(vectorMsg=sqrt_serialized_msg)

        return response

    def DivEncVector(self, request, context):
        # get the dividend vector
        dividend_enc_msg = request.dividendMsg
        dividend_enc_vector = ts.ckks_vector_from(self.sk_ctx, dividend_enc_msg)
        dividend_dec_vector = dividend_enc_vector.decrypt()
        # get the divisor vector
        divisor_enc_msg = request.divisorMsg
        divisor_enc_vector = ts.ckks_vector_from(self.sk_ctx, divisor_enc_msg)
        divisor_dec_vector = divisor_enc_vector.decrypt()
        # get the division(dividend/divisor)
        div_dec_vector = np.divide(dividend_dec_vector, divisor_dec_vector)

        # make response and return
        div_plain_vector = ts.plain_tensor(div_dec_vector)
        div_enc_vector = ts.ckks_vector(self.sk_ctx,div_plain_vector)
        sqrt_serialized_msg = div_enc_vector.serialize()
        response = request_keyServer_pb2.vectorResult(vectorMsg=sqrt_serialized_msg)

        return response
