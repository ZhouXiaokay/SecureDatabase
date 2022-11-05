import time

import grpc
import numpy as np
import tenseal as ts
import torch
import sys
from transmission.tenseal import tenseal_aggregate_server_pb2, tenseal_aggregate_server_pb2_grpc
from transmission.utils import flatten_tensors, unflatten_tensors


class Client:

    def __init__(self, server_address, client_rank, ctx_file):
        self.server_address = server_address
        self.client_rank = client_rank

        context_bytes = open(ctx_file, "rb").read()
        self.ctx = ts.context_from(context_bytes)

        self.max_msg_size = 1000000000
        self.options = [('grpc.max_send_message_length', self.max_msg_size),
                        ('grpc.max_receive_message_length', self.max_msg_size)]
        channel = grpc.insecure_channel(self.server_address, options=self.options)
        self.stub = tenseal_aggregate_server_pb2_grpc.AggregationServerServiceStub(channel)

    def __sum_encrypted(self, plain_vector):
        # print(">>> client sum encrypted start")

        # encrypt
        encrypt_start = time.time()
        enc_vector = ts.ckks_vector(self.ctx, plain_vector)
        encrypt_time = time.time() - encrypt_start

        # print("size of msg: {} bytes".format(sys.getsizeof(enc_vector.serialize())))

        # create request
        request_start = time.time()
        request = tenseal_aggregate_server_pb2.aggr_params(
            client_rank=self.client_rank,
            params_msg=enc_vector.serialize()
        )
        request_time = time.time() - request_start

        # comm with server
        comm_start = time.time()
        # print("start comm with server, time = {}".format(time.asctime(time.localtime(time.time()))))
        response = self.stub.sum_encrypted(request)
        comm_time = time.time() - comm_start

        # deserialize summed vector from response
        deserialize_start = time.time()
        assert self.client_rank == response.client_rank
        summed_encrypted_vector = ts.ckks_vector_from(self.ctx, response.params_msg)
        deserialize_time = time.time() - deserialize_start

        # decrypt vector
        decrypt_start = time.time()
        summed_plain_vector = summed_encrypted_vector.decrypt()
        decrypt_time = time.time() - decrypt_start

        # print(">>> client sum encrypted end, cost {:.2f} s: encryption {:.2f} s, create request {:.2f} s, "
        #       "comm with server {:.2f} s, deserialize {:.2f} s, decryption {:.2f} s"
        #       .format(time.time() - encrypt_start, encrypt_time, request_time,
        #               comm_time, deserialize_time, decrypt_time))

        return summed_plain_vector

    def transmit(self, params_list, operator="sum"):

        trans_start = time.time()
        # received:list, received tensors convert received to tensors
        received = self.__sum_encrypted(params_list) if operator == "sum" else None
        # print(">>> client transmission cost {:.2f} s".format(time.time() - trans_start))
        return received


if __name__ == '__main__':
    serv_address = "127.0.0.1:59000"
    ctx_file = "../../transmission/ts_ckks.config"
    client_rank = 0

    client = Client(serv_address, client_rank, ctx_file)

