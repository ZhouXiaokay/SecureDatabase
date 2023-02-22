import grpc
import transmission.tenseal.tenseal_aggregate_server_pb2 as tenseal_aggregate_server_pb2
import transmission.tenseal.tenseal_aggregate_server_pb2_grpc as tenseal_aggregate_server_pb2_grpc
import tenseal as ts
import time
import numpy as np
import torch.optim as optim
import torch
from transmission.utils import flatten_tensors
import math
from distutils.util import strtobool


class AggregateServer(tenseal_aggregate_server_pb2_grpc.AggregateServerServiceServicer):

    def __init__(self, num_clients, pk_ctx_file, model):
        # initial params
        self.db_num = 3
        self.num_clients = num_clients
        self.update_size = 2
        pk_ctx_bytes = open(pk_ctx_file, "rb").read()
        self.pk_ctx = ts.context_from(pk_ctx_bytes)
        self.reline_keys = self.pk_ctx.relin_keys()
        self.sleep_time = 0.01
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

        # for ID Psi
        self.all_client_ids = []
        self.cid_list = []
        self.final_intersection = set()
        self.set_completed = False
        self.intersect_completed = False

        # for rsa psi
        self.num_psi_request = 0
        self.num_psi_response = 0
        self.psi_cid_list = []
        self.psi_IP_list = []
        self.psi_store_psi_result_list = []
        self.num_psi_participators = 0
        self.total_psi_rounds = 1000000
        self.current_psi_round = 0
        self.initial_participators = []
        self.waiting_for_participators_status = False
        self.waiting_for_initialize = False
        self.group_index_list = []
        self.psi_comm_IP_index = []
        self.psi_update_status = False
        self.psi_check_result_count = 0
        self.psi_final_result_status = False
        self.psi_final_result = None

    def __reset_psi_status_per_round(self):
        self.num_psi_request = 0
        self.num_psi_response = 0
        self.psi_check_result_count = 0
        self.psi_update_status = False

    def __reset_all_psi_status(self):
        self.num_psi_request = 0
        self.num_psi_response = 0
        self.psi_cid_list = []
        self.psi_IP_list = []
        self.psi_store_psi_result_list = []
        self.num_psi_participators = 0
        self.total_psi_rounds = 1000000
        self.current_psi_round = 0
        self.initial_participators = []
        self.waiting_for_participators_status = False
        self.waiting_for_initialize = False
        self.group_index_list = []
        self.psi_comm_IP_index = []
        self.psi_update_status = False
        self.psi_check_result_count = 0
        self.psi_final_result_status = False
        self.psi_final_result = None

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

    def __reset_id_intersection(self):
        self.n_sum_response = 0
        self.n_sum_request = 0
        self.all_client_ids = []
        self.cid_list = []
        self.final_intersection = set()
        self.set_completed = False
        self.intersect_completed = False

    def __reset_rsa_intersection(self):
        self.n_sum_response = 0
        self.waiting_status = False
        self.index_completed = False
        self.cid_list = []
        self.num_psi_participators = 0

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
        self.latest_model_params.data = latest_params.data

    def __sum_encrypted_params(self):
        self.pk_ctx.relin_keys()
        self.sum_count = sum(self.count_dict.values())
        self.accum_count = sum(self.accum_count_list)
        # ratio = 1 - self.accum_count / self.sum_count

        sum_enc_params = sum(self.params_list)
        # Bootstrapping
        # latest_enc_model_params = self.latest_model_params.decrypt()
        # latest_model_params = ts.ckks_vector(self.pk_ctx, latest_enc_model_params)
        # latest_enc_params = ratio * self.latest_model_params
        # latest_enc_params += 1 / self.sum_count * sum_enc_params

        latest_enc_params = 1 / self.accum_count * sum_enc_params

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

    def get_intersection(self, request, context):
        """

        :param request: request
        :param context: context
        :return: id_intersection result
        """

        cid = request.cid
        qid = request.qid
        client_ids = request.request_msg

        if cid not in self.cid_list:
            self.cid_list.append(cid)
            self.all_client_ids.append(client_ids)
            self.n_sum_request += 1
        else:
            raise ValueError('Already requested.')

        while (self.n_sum_request % self.db_num != 0):
            time.sleep(self.sleep_time)

        if cid == self.cid_list[-1]:
            for index, value in enumerate(self.all_client_ids):
                value_set = set(value)
                self.all_client_ids[index] = value_set
            self.set_completed = True

        while (not self.set_completed):
            time.sleep(self.sleep_time)

        if cid == self.cid_list[-1]:
            for index, value in enumerate(self.all_client_ids):
                if index == len(self.all_client_ids) - 1:
                    break
                if index == 0:
                    self.final_intersection = self.all_client_ids[index].intersection(self.all_client_ids[index + 1])
                else:
                    self.final_intersection = self.final_intersection.intersection(self.all_client_ids[index + 1])

            self.intersect_completed = True

        while (not self.intersect_completed):
            time.sleep(self.sleep_time)

        response = tenseal_aggregate_server_pb2.intersection_response(
            cid=cid,
            qid=qid,
            response_msg=list(self.final_intersection)
        )
        self.n_sum_response += 1

        while (self.n_sum_response % self.db_num != 0):
            time.sleep(self.sleep_time)

        self.__reset_id_intersection()

        return response

    def get_intersection_sequence_index(self, request, context):
        """

        :param request: request
        :param context: response
        :return: participator index and total-participator number
        """
        first_requested = None
        cid = request.cid
        qid = request.qid

        if len(self.cid_list) == 0:
            first_requested = cid

        if cid not in self.cid_list:
            self.cid_list.append(cid)
        else:
            raise ValueError('Already requested.')

        # Waiting for all participators
        if cid == first_requested:
            time.sleep(10)
            self.waiting_status = True
        while (not self.waiting_status):
            time.sleep(self.sleep_time)

        print("All participator collected.")
        if cid == self.cid_list[0]:
            self.cid_list.sort()
            self.index_completed = True

        while (not self.index_completed):
            time.sleep(self.sleep_time)

        num_participators = len(self.cid_list)

        response = tenseal_aggregate_server_pb2.intersection_sequence_index(
            cid=cid,
            qid=qid,
            sequence_index=self.cid_list.index(cid),
            total_participator=num_participators
        )
        self.n_sum_response += 1
        while (self.n_sum_response % num_participators != 0):
            time.sleep(self.sleep_time)

        self.__reset_rsa_intersection()
        return response

    def __total_psi_rounds(self):
        if self.num_psi_participators <= 1:
            self.total_psi_rounds = 1
        else:
            self.total_psi_rounds = max(int(math.log2(self.num_psi_participators - 1)), 0) + 1

    def __update_group_index_list(self):
        self.group_index_list.clear()
        for i in range(len(self.psi_cid_list)):
            self.group_index_list.append(int((i // math.pow(2, self.current_psi_round))))

    def __get_psi_comm_IP(self):
        comm_IP_list = [-1 for _ in range(self.num_psi_participators)]
        i = 0
        while (i < self.num_psi_participators):
            j = i + 1
            if self.psi_store_psi_result_list[i] == True:
                if i in comm_IP_list:
                    comm_IP_list[i] = comm_IP_list.index(i)
                    i = j
                    continue
                while (j < self.num_psi_participators):
                    if self.psi_store_psi_result_list[j] == True:
                        comm_IP_list[i] = j
                        break
                    j += 1
            i = j

        self.psi_comm_IP_index = comm_IP_list

    def __update_store_psi_result_status_regular(self):
        self.psi_store_psi_result_list.clear()
        id_set = set()
        for group_index in self.group_index_list:
            if group_index not in id_set:
                self.psi_store_psi_result_list.append(True)
                id_set.add(group_index)
            else:
                self.psi_store_psi_result_list.append(False)

    def __generate_agg_server_status(self, cid):
        data_server_index = self.psi_cid_list.index(cid)
        if self.psi_comm_IP_index[data_server_index] == -1:
            comm_IP = 0
        else:
            comm_IP = self.psi_IP_list[self.psi_comm_IP_index[data_server_index]]
        agg_server_status = [self.num_psi_participators, self.total_psi_rounds, self.current_psi_round,
                             data_server_index, self.group_index_list[data_server_index],
                             self.psi_store_psi_result_list[data_server_index], comm_IP]

        return agg_server_status

    def get_agg_server_status(self, request, context):
        cid = request.cid
        qid = request.qid
        data_server_status = request.data_server_status
        carry_psi_final_result = request.carry_psi_final_result
        psi_final_result = request.psi_final_result
        time.sleep(0.1)

        assert self.current_psi_round == int(data_server_status[2])
        if self.current_psi_round == 0:
            first_request_cid = None
            if (int(data_server_status[2]) == 0) and (cid not in self.psi_cid_list):
                if len(self.psi_cid_list) == 0:
                    first_request_cid = cid
                self.psi_cid_list.append(cid)
                self.psi_IP_list.append(data_server_status[0])
                self.psi_store_psi_result_list.append(bool(data_server_status[1]))
            else:
                raise ValueError(f"DataServer {cid} already requested.")

            # Waiting 8s for other participators to join
            if cid == first_request_cid:
                time.sleep(8)
                self.waiting_for_participators_status = True
            while not self.waiting_for_participators_status:
                time.sleep(self.sleep_time)
            assert len(self.psi_cid_list) == len(self.psi_IP_list) == len(self.psi_store_psi_result_list)

            if cid == first_request_cid:
                self.num_psi_participators = len(self.psi_cid_list)
                self.__total_psi_rounds()
                print("All participator collected.")
                # print(self.psi_cid_list)
                # print(self.psi_IP_list)
                print(f"num_psi_participators : {self.num_psi_participators}")
                print(f"Total psi rounds: {self.total_psi_rounds}")
                self.waiting_for_initialize = True
            while not self.waiting_for_initialize:
                time.sleep(self.sleep_time)

        self.num_psi_request += 1
        # waiting_time_count = 0
        while (self.num_psi_request % self.num_psi_participators != 0):
            time.sleep(self.sleep_time)

        if carry_psi_final_result == True:
            self.psi_final_result = psi_final_result
            self.psi_final_result_status = True
        self.psi_check_result_count += 1

        # print(carry_psi_final_result)
        while (self.psi_check_result_count % self.num_psi_participators != 0):
            time.sleep(self.sleep_time)
        # print(self.psi_final_result_status)

        if (self.current_psi_round == self.total_psi_rounds == int(data_server_status[2])) and \
                (self.psi_final_result_status == True):
            response = tenseal_aggregate_server_pb2.agg_server_status_response(
                cid=cid,
                qid=qid,
                agg_server_status=[],
                carry_psi_final_result=self.psi_final_result_status,
                psi_final_result=self.psi_final_result
            )
            self.num_psi_response += 1
            while (self.num_psi_response % self.num_psi_participators != 0):
                time.sleep(self.sleep_time)
            time.sleep(self.sleep_time)
            self.__reset_all_psi_status()

            return response

        if cid == self.psi_cid_list[0]:
            self.current_psi_round += 1
            self.__update_group_index_list()
            # print(self.group_index_list)
            self.__get_psi_comm_IP()
            # print(self.psi_store_psi_result_list)
            # print(self.psi_comm_IP_index)
            # print(f"group_index: {self.group_index_list}")
            self.__update_store_psi_result_status_regular()
            # print(self.psi_store_psi_result_list)
            self.psi_update_status = True

        while not self.psi_update_status:
            time.sleep(self.sleep_time)

        agg_server_status = self.__generate_agg_server_status(cid)
        # print(agg_server_status)
        agg_server_status_str = []
        for item in agg_server_status:
            agg_server_status_str.append(str(item))

        response = tenseal_aggregate_server_pb2.agg_server_status_response(
            cid=cid,
            qid=qid,
            agg_server_status=agg_server_status_str,
            carry_psi_final_result=carry_psi_final_result,
            psi_final_result=psi_final_result
        )

        self.num_psi_response += 1
        while (self.num_psi_response % self.num_psi_participators != 0):
            time.sleep(self.sleep_time)

        self.__reset_psi_status_per_round()
        return response
