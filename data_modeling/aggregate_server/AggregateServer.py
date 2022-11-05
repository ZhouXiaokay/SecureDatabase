import grpc
import transmission.tenseal.tenseal_aggregate_server_pb2 as tenseal_aggregate_server_pb2
import transmission.tenseal.tenseal_aggregate_server_pb2_grpc as tenseal_aggregate_server_pb2_grpc
import tenseal as ts
import time


class AggregateServer(tenseal_aggregate_server_pb2_grpc.AggregationServerServiceServicer):

    def __init__(self, num_clients, pk_ctx_file):
        self.num_clients = num_clients
        pk_ctx_bytes = open(pk_ctx_file, "rb").read()
        self.pk_ctx = ts.context_from(pk_ctx_bytes)
        self.sleep_time = 0.1
        self.n_sum_request = 0
        self.n_sum_response = 0
        self.n_sum_round = 0
        self.params_list = []
        self.sum_completed = False
        self.sum_enc_params = []

    def __reset(self):
        self.sum_completed = False
        self.sum_enc_params.clear()
        self.params_list.clear()
        self.n_sum_request = 0
        self.n_sum_response = 0

    def __sum_encrypted_params(self):
        self.sum_enc_params.append(sum(self.params_list))

    def sum_encrypted(self, request, context):
        client_rank = request.client_rank
        enc_params_msg = request.params_msg
        enc_params_vector = ts.ckks_vector_from(self.pk_ctx, enc_params_msg)
        self.params_list.append(enc_params_vector)
        self.n_sum_request += 1
        while self.n_sum_request % self.num_clients != 0:
            time.sleep(self.sleep_time)

        if client_rank == self.num_clients - 1:
            self.__sum_encrypted_params()
            self.sum_completed = True
        while not self.sum_completed:
            time.sleep(self.sleep_time)
        # create response
        enc_sum_params_msg = self.sum_enc_params[0].serialize()
        response = tenseal_aggregate_server_pb2.aggr_params(client_rank=client_rank,
                                                            params_msg=enc_sum_params_msg)
        # wait until all response created
        self.n_sum_response = self.n_sum_response + 1
        while self.n_sum_response % self.num_clients != 0:
            time.sleep(self.sleep_time)

        # clear cache
        if client_rank == self.num_clients - 1:
            self.__reset()

        # wait until cache for sum reset
        self.n_sum_round = self.n_sum_round + 1
        while self.n_sum_round % self.num_clients != 0:
            time.sleep(self.sleep_time)

        return response
