import grpc
import transmission.tenseal.tenseal_aggregate_server_pb2 as tenseal_aggregate_server_pb2
import transmission.tenseal.tenseal_aggregate_server_pb2_grpc as tenseal_aggregate_server_pb2_grpc
import tenseal as ts
import time
import numpy as np
import torch.optim as optim
import torch
from transmission.utils import flatten_tensors
import pickle
import copy

class AggregateServer(tenseal_aggregate_server_pb2_grpc.AggregationServerServiceServicer):

    def __init__(self, num_clients, pk_ctx_file, model):
        # initial params
        self.num_clients = num_clients
        self.update_size = 2
        pk_ctx_bytes = open(pk_ctx_file, "rb").read()
        self.pk_ctx = ts.context_from(pk_ctx_bytes)
        self.reline_keys = self.pk_ctx.relin_keys()
        self.sleep_time = 0.1
        ###########
        self.global_model = model
        self.optimizer = optim.Adam(self.global_model.parameters())
        self.latest_model_params = self.__get_init_params()

        # for sum_encrypted
        self.n_sum_request = 0
        self.n_sum_response = 0
        self.n_sum_round = 0
        self.params_list = []
        self.sum_enc_params = []
        self.sum_completed = False

        self.count_dict = {}
        self.sum_count = 0
        self.accum_count_list = []
        self.accum_count = 0

        # for boolean_is_update
        self.clients_list = [i for i in range(num_clients)]
        self.update_clients_list = []
        self.n_update_request = 0
        self.n_update_response = 0
        self.n_update_round = 0
        self.get_update_clients_completed = False

    def __reset_sum(self):
        self.sum_completed = False
        self.sum_enc_params.clear()
        self.params_list.clear()
        self.n_sum_request = 0
        self.n_sum_response = 0
        # reset count
        # self.count_list.clear()
        self.sum_count = 0
        self.accum_count_list.clear()
        self.accum_count = 0

    def __reset_update(self):
        self.get_update_clients_completed = False
        self.n_update_request = 0
        self.n_update_response = 0

        self.n_sum_round = 0

    def __get_init_params(self):
        param_list = []
        for group in self.optimizer.param_groups:
            for p in group['params']:
                with torch.no_grad():
                    param_list.append(p)
        param_flat_tensor = flatten_tensors(param_list).detach()
        plain_params_tensor = ts.plain_tensor(param_flat_tensor)
        enc_param_vector = ts.ckks_vector(self.pk_ctx, plain_params_tensor)
        return enc_param_vector

    def __update_global_model_params(self, latest_params):
        self.latest_model_params = latest_params

    def __sum_encrypted_params(self):
        self.pk_ctx.relin_keys()
        self.sum_count = sum(self.count_dict.values())
        self.accum_count = sum(self.accum_count_list)
        ratio = 1 - self.accum_count / self.sum_count
        ratio = round(ratio, 4)

        sum_enc_params = sum(self.params_list)
        latest_enc_params = 1 / self.sum_count * sum_enc_params
        latest_enc_params += ratio * self.latest_model_params

        self.sum_enc_params.append(latest_enc_params)
        self.__update_global_model_params(latest_enc_params)

    def __generate_update_clients(self):
        self.update_size = np.random.randint(low=2, high=4)
        self.update_clients_list = np.random.choice(self.clients_list, self.update_size, replace=False).tolist()

    def boolean_is_update(self, request, context):
        client_rank = request.client_rank
        sample_num = request.sample_num
        self.count_dict[client_rank] = sample_num
        # wait until receiving all clients
        self.n_update_request += 1
        while self.n_update_request % self.num_clients != 0:
            time.sleep(self.sleep_time)

        if client_rank == self.num_clients - 1:
            self.__generate_update_clients()
            self.get_update_clients_completed = True

        while not self.get_update_clients_completed:
            time.sleep(self.sleep_time)

        # create response
        flag = bool(client_rank in self.update_clients_list)
        global_params_msg = self.latest_model_params.serialize()
        if not flag:
            global_params_msg = ts.ckks_vector(self.pk_ctx, [0]).serialize()
        response = tenseal_aggregate_server_pb2.update_response(flag=flag,
                                                                params_msg=global_params_msg)
        # wait until all response created
        self.n_update_response = self.n_update_response + 1
        while self.n_update_response % self.num_clients != 0:
            time.sleep(self.sleep_time)

        # clear cache
        if client_rank == self.num_clients - 1:
            self.__reset_update()

        # wait until cache for sum reset
        self.n_update_round = self.n_update_round + 1
        while self.n_update_round % self.num_clients != 0:
            time.sleep(self.sleep_time)

        return response

    def sum_encrypted(self, request, context):
        client_rank = request.client_rank
        sample_num = request.sample_num
        enc_params_msg = request.params_msg
        enc_params_vector = ts.ckks_vector_from(self.pk_ctx, enc_params_msg)
        self.params_list.append(enc_params_vector)
        self.accum_count_list.append(sample_num)
        self.n_sum_request += 1
        while self.n_sum_request % self.update_size != 0:
            time.sleep(self.sleep_time)

        # if client_rank == self.update_size - 1:
        if client_rank == self.update_clients_list[0]:
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
        while self.n_sum_response % self.update_size != 0:
            time.sleep(self.sleep_time)

        # clear cache
        # if client_rank == self.update_size - 1:
        if client_rank == self.update_clients_list[0]:
            self.__reset_sum()

        # wait until cache for sum reset
        self.n_sum_round = self.n_sum_round + 1
        while self.n_sum_round % self.update_size != 0:
            time.sleep(self.sleep_time)

        return response
